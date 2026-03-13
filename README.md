# Berg Little Printer — Reverse-Engineered Zigbee Protocol

Полный разбор протокола связи Berg Cloud Bridge с термопринтером Little Printer.
Цель — управление принтером напрямую через ESP32 с Zigbee-адаптером, без облака Berg Cloud.

---

## Оглавление

- [Архитектура](#архитектура)
- [Шифрование и безопасность](#шифрование-и-безопасность)
- [Адресация устройств](#адресация-устройств)
- [Присоединение принтера к сети](#присоединение-принтера-к-сети)
- [Несколько принтеров](#несколько-принтеров)
- [Zigbee-параметры сети](#zigbee-параметры-сети)
- [Протокол передачи данных](#протокол-передачи-данных)
- [Коды ответов и события](#коды-ответов-и-события)
- [Реализация на ESP32](#реализация-на-esp32)
- [Выбор Zigbee-чипа/модуля](#выбор-zigbee-чипамодуля)
- [Генерация Link Key из Claim Code](#генерация-link-key-из-claim-code)
- [Бинарный payload команды печати](#бинарный-payload-команды-печати)
- [RLE-кодирование изображений](#rle-кодирование-изображений)
- [Команды принтера](#команды-принтера)
- [WebSocket JSON-протокол (Bridge ↔ Server)](#websocket-json-протокол-bridge--server)
- [Структура бинарных событий от принтера](#структура-бинарных-событий-от-принтера)
- [Ключевые файлы](#ключевые-файлы)

---

## Архитектура

Berg Cloud Bridge — это Linux-устройство (ARM, на базе Chumby) с Python-демоном `weminuche_bridge.pyc`:

```
Berg Cloud (WebSocket wss://bridge.bergcloud.com:443)
         │
         ▼
┌─────────────────────┐
│   Berg Bridge       │
│   (Linux + Python)  │
│                     │
│  weminuche_bridge   │ ◄── Главный демон
│  berg_cloud_socket  │ ◄── WebSocket-клиент (SSL, клиентский сертификат)
│  api.py             │ ◄── Zigbee API (отправка блоков)
│  framework.py       │ ◄── ZCL-парсинг, управление стеком
│  trust_center.py    │ ◄── Управление ключами шифрования
│  ezsp.py            │ ◄── EZSP протокол (SPI к NCP)
└─────────┬───────────┘
          │ Zigbee (EZSP over SPI)
          ▼
┌─────────────────────┐
│  Zigbee NCP         │
│  (Silicon Labs       │
│   EM35x / EFR32)    │
└─────────┬───────────┘
          │ IEEE 802.15.4 (2.4 GHz)
          ▼
┌─────────────────────┐
│  Little Printer     │
│  (Zigbee End Device)│
└─────────────────────┘
```

---

## Шифрование и безопасность

**Да, шифрование используется.** Это критически важный момент для самостоятельной реализации.

### Уровень безопасности

| Параметр | Значение |
|----------|----------|
| Security Profile | `CUSTOM_SECURITY_PROFILE` (255) |
| Security Level | **5** (AES-128-CCM с MIC-32) |
| Max APS payload | 82 байт (с шифрованием, vs 100 без) |

### Сетевой ключ (Network Key)

- Генерируется случайно при создании сети (`_createRandomKey()`)
- 16 байт AES-128
- **Ротация каждые 60 минут** — бридж автоматически обновляет и переключает ключ
- Все устройства в сети используют один сетевой ключ

### Link Key (ключ устройства)

Это самая важная часть для подключения принтера:

1. При **присоединении нового устройства** срабатывает `callback_ezspTrustCenterJoinHandler`
2. Если статус = `STANDARD_SECURITY_UNSECURED_JOIN` и решение = `USE_PRECONFIGURED_KEY`, бридж генерирует событие `encryption_key_required` с `device_address` (EUI64 принтера)
3. Это событие отправляется в облако Berg Cloud
4. Облако отвечает командой `add_device_encryption_key` с параметрами:
   - `device_address` — EUI64 принтера (hex-строка)
   - `encryption_key` — 16-байтный link key (Base64)
5. Бридж вызывает `TCAddOrUpdateKey(eui64, key)` и после этого инициирует ротацию сетевого ключа

### Политики безопасности

| Политика | Значение |
|----------|----------|
| Trust Center Policy | `ALLOW_PRECONFIGURED_KEY_JOINS` |
| Link Key Request | **Запрещён** |
| App Key Request | **Запрещён** |

### Как генерируется Link Key

Из анализа сервера [Sirius](https://github.com/nordprojects/sirius) стала ясна полная цепочка:

1. Принтер при первом включении отправляет свой EUI64
2. Из EUI64 вычисляется **hardware_xor** (3 байта) — детерминированный хеш
3. По hardware_xor находится **claim code** (16 символов base32, напечатан на наклейке принтера)
4. Из claim code извлекается **40-битный secret**
5. Secret пропускается через **AES-ECB с солью** → 16-байтный link key

Подробнее — в разделе [Генерация Link Key из Claim Code](#генерация-link-key-из-claim-code).

### Что это значит для ESP32

Link key **детерминирован** и зависит только от claim code принтера. Варианты получения:

1. **Если есть claim code** (наклейка на принтере, формат `xxxx-xxxx-xxxx-xxxx`) — вычислить link key по алгоритму из Sirius
2. **Если бридж уже был сопряжён** — claim code сохранён в базе сервера, link key уже в NCP
3. **Перехватить ключ** из дампа оригинального бриджа (если он сохранён в NCP)
4. **Использовать well-known key** — `ZigBeeAlliance09` (`5A6967426565416C6C69616E63653039`) как preconfigured key

> **Наиболее реалистичный сценарий**: использовать claim code с наклейки на принтере, вычислить из него link key по алгоритму ниже, и загрузить в Trust Center ESP32.

---

## Адресация устройств

### EUI64 (IEEE MAC-адрес)

Каждое Zigbee-устройство имеет уникальный 8-байтный адрес **EUI64**, прошитый в чип.

- Формат: `0x00124B001234ABCD` (hex, 16 символов)
- Хранится в little-endian tuple в коде: `(0xCD, 0xAB, 0x34, 0x12, 0x00, 0x4B, 0x12, 0x00)`
- Преобразование: `byte_tuple.eui64ToHexString()` — разворачивает и форматирует

### Node ID (короткий сетевой адрес)

- 2-байтный адрес, назначаемый при присоединении к сети
- Используется для маршрутизации пакетов
- Преобразование: `emberLookupNodeIdByEui64(eui64)` → Node ID
- Если Node ID = 0 → устройство не найдено → `RSP_EUI64_NOT_FOUND`

### Как узнать адрес принтера

1. **При присоединении к сети**: вызывается `callback_ezspChildJoinHandler(index, joining, childID, childEui64, childType)`
   - `childEui64` — это EUI64 принтера
   - `childID` — это Node ID
   - `joining = True` — устройство вошло в сеть

2. **Из таблицы дочерних устройств**: `ezspGetChildData(index)` → `(childId, childEui64, childType)`

3. **Из таблицы адресов**: `emberGetAddressTableRemoteEui64(index)` → EUI64

4. **По heartbeat-событиям**: принтер периодически шлёт heartbeat (event code = 1), и его EUI64 приходит как `senderEui64`

### Для ESP32

При включении принтера в сеть:
```
Принтер → Association Request → Координатор (ESP32)
Координатор назначает Node ID
callback: childJoinHandler(childEui64)  ← запоминаем этот адрес
```

---

## Присоединение принтера к сети

### Последовательность действий

1. **Сформировать сеть** как координатор:
   ```
   scanForUnusedPanId(channels)  → выбрать свободный PAN ID
   formNetwork(parameters)       → создать сеть
   ```

2. **Разрешить присоединение**:
   ```
   emberPermitJoining(255)       → 255 = бесконечно
   ```

3. **Принтер сам ищет сеть** с Profile ID 0xC000 на одном из каналов [11, 14, 15, 19, 20, 24, 25]

4. **При присоединении** срабатывает Trust Center Join Handler

5. **Добавить link key** (если требуется)

6. **Принтер отправляет** `EVENT_DID_POWER_ON` (код 3)

7. **Бридж/ESP32 регистрирует** устройство в `event_sources`

### Параметры создания сети

| Параметр | Значение |
|----------|----------|
| Extended PAN ID | Префикс `0x42455247` ("BERG") + случайные 32 бита |
| Radio Power | 8 dBm |
| TX Power Mode | `EMBER_TX_POWER_MODE_BOOST` |
| Каналы | 11, 14, 15, 19, 20, 24, 25 |
| Stack Profile | 2 (Zigbee PRO) |
| Disable Relay | 1 |

### Выбор канала

Бридж делает energy scan на всех каналах, собирает все каналы в пределах **10 dBm** от минимума (`ENERGY_BAND = 10`) и выбирает **случайный** канал из этой группы:

```
energyScanRequest(0)
→ собрать результаты
→ выбрать канал с lowest dBm
→ channelChangeRequest(selected_channel)
```

---

## Несколько принтеров

Система поддерживает до **8 устройств** одновременно:

| Ресурс | Лимит |
|--------|-------|
| Address Table | 8 записей |
| Key Table | 16 записей |
| Trust Center Cache | 2 записи |

### Как это работает

- Каждый принтер имеет уникальный EUI64
- При подключении каждый получает свой Node ID
- Команды отправляются unicast на конкретный Node ID
- Бридж отслеживает активные устройства в `event_sources` (dict: EUI64 → [first_seen, last_seen])
- Heartbeat timeout = **30 секунд** на стороне бриджа (`HEARTBEAT_TIMEOUT = 30` в `berg_cloud_socket_api.pyc.py`), **60 секунд** на стороне Sirius-сервера (`mark_dead_by_timeout` в `protocol_loop.py`)

### Маршрутизация к нескольким принтерам

```python
nodeId = emberLookupNodeIdByEui64(target_printer_eui64)
sendUnicast(EMBER_OUTGOING_DIRECT, nodeId, apsFrame, message)
```

Каждая команда содержит `device_address` (EUI64 принтера), так что можно управлять каждым принтером независимо.

---

## Zigbee-параметры сети

### Endpoint Configuration

| Параметр | Значение | Hex |
|----------|----------|-----|
| Profile ID | 49152 | `0xC000` |
| Cluster ID (Weminuche) | 65280 | `0xFE00` |
| Cluster ID (Basic) | 0 | `0x0000` |
| Manufacturer ID | 4098 | `0x1002` |
| Source Endpoint | 1 | `0x01` |
| Destination Endpoint | 1 | `0x01` |
| Device ID | 1 | `0x0001` |
| Device Version | 0 | `0x00` |

### Endpoint Definition

```
Endpoint 1:
  Profile: 0xC000 (кастомный — НЕ стандартный ZHA 0x0104)
  In Clusters:  [0x0000 (Basic), 0xFE00 (Weminuche)]
  Out Clusters: [0x0000 (Basic), 0xFE00 (Weminuche)]
```

### Каналы

Используется подмножество каналов IEEE 802.15.4:

| Канал | Частота |
|-------|---------|
| 11 | 2405 MHz |
| 14 | 2420 MHz |
| 15 | 2425 MHz |
| 19 | 2445 MHz |
| 20 | 2450 MHz |
| 24 | 2470 MHz |
| 25 | 2475 MHz |

---

## Протокол передачи данных

### ZCL Frame (Bridge → Printer)

```
┌───────────┬────────────┬──────┬───────────┬───────────────────┐
│ FrameCtl  │  MfgCode   │ Seq  │  CmdID    │  Payload          │
│  1 byte   │  2 bytes   │ 1 b  │  1 byte   │  1 + ≤512 bytes   │
│  0x05     │  0x0210    │ var  │  0x01     │  BlockID + Data   │
└───────────┴────────────┴──────┴───────────┴───────────────────┘
```

### Frame Control (0x05)

```
Bit 0: 1 = Cluster-specific command
Bit 1: 0 = Client-to-server
Bit 2: 1 = Manufacturer-specific
Bit 3: 0 = Direction: client-to-server
```

`0x05 = ZCL_CLUSTER_SPECIFIC_COMMAND | ZCL_FRAME_CONTROL_CLIENT_TO_SERVER | ZCL_MANUFACTURER_SPECIFIC_MASK`

### Manufacturer Code

Кодируется в **little-endian**: `0x1002` → байты `0x02, 0x10`

### Логика нарезки и отправки

```
blockID = 0
while есть данные:
    chunk = read(512 байт)
    payload = pack('>B', blockID) + chunk    # blockID в big-endian
    отправить через _blockingWrite(nodeId, payload)
    
    blockID += 1
    if blockID > 255:
        blockID = 1    # wrap: 0 → 1..255 → 1..255 → ...
```

### Параметры передачи

| Параметр | Значение |
|----------|----------|
| Размер блока | 512 байт данных + 1 байт blockID |
| Макс. попыток на блок | 4 |
| Задержка между попытками | 1 секунда |
| Таймаут отправки | 5 секунд |
| Таймаут ответа | 5 секунд |
| Фрагментация (APS) | Включена для пакетов > 82 байт |
| Размер буфера фрагментации | 1024 байт |
| Макс. фрагментов | 30 |
| Окно фрагментации | 8 |
| Fragment delay | 0 мс |

### APS Options

```
EMBER_APS_OPTION_RETRY | EMBER_APS_OPTION_ENABLE_ROUTE_DISCOVERY | EMBER_APS_OPTION_ENABLE_ADDRESS_DISCOVERY
```

При шифровании добавляется `EMBER_APS_OPTION_ENCRYPTION`.

---

## Коды ответов и события

### Коды ответов от принтера (полная таблица)

Код ответа содержится в `data[10]` входящего сообщения. Источники кодов указаны в столбце:

| Код | Hex | Константа | Значение | Источник |
|-----|-----|-----------|----------|----------|
| 0 | 0x00 | `RSP_SUCCESS` | Успех | bridge |
| 1 | 0x01 | `RSP_EUI64_NOT_FOUND` | EUI64 не найден в таблице | bridge |
| 2 | 0x02 | `RSP_FAILED_NETWORK` | Ошибка сети | bridge |
| 32 | 0x20 | `RSP_INVALID_SEQUENCE` | Неверная последовательность блоков | bridge |
| 48 | 0x30 | `RSP_BUSY` | Принтер занят | protocol.proto |
| 128 | 0x80 | `RSP_INVALID_SIZE` | Неверный размер блока | bridge |
| 129 | 0x81 | `RSP_INVALID_DEVICETYPE` | Неверный тип устройства | bridge |
| 130 | 0x82 | `RSP_FILESYSTEM_ERROR` | Ошибка файловой системы | bridge |
| 144 | 0x90 | `RSP_FILESYSTEM_INVALID_ID` | Невалидный file ID | protocol.proto |
| 145 | 0x91 | `RSP_FILESYSTEM_NO_FREE_HANDLES` | Нет свободных файловых дескрипторов | protocol.proto |
| 146 | 0x92 | `RSP_FILESYSTEM_WRITE_ERROR` | Ошибка записи в ФС | protocol.proto |
| 224 | 0xE0 | `RSP_QUEUE_FULL` | Очередь команд переполнена (на бридже) | bridge |
| 255 | 0xFF | `RSP_BRIDGE_ERROR` | Общая ошибка бриджа | bridge (catch-all) |

### События от принтера

Входящие сообщения с кластера 0xFE00 парсятся по `eventCode` (2 байта, little-endian, смещение 0 от payload):

| Код | Hex | Событие | Описание |
|-----|-----|---------|----------|
| 1 | 0x0001 | `EVENT_HEARTBEAT` | Периодический пульс (payload: 4 байта uptime) |
| 2 | 0x0002 | `EVENT_DID_PRINT` | Печать завершена (payload: type + print_id) |
| 3 | 0x0003 | `EVENT_DID_POWER_ON` | Принтер включился (payload: firmware info) |
| 128 | 0x0080 | Command Response | Ответ на команду (код в data[10]) |
| 0xA000 | — | `BC_EVENT_PRODUCT_ANNOUNCE` | Анонс продукта (product_id 16 байт + version) |
| 0xE0xx | — | `BC_EVENT_START_BINARY` | Бинарное событие от устройства |
| 0xE1xx | — | `BC_EVENT_START_PACKED` | Упакованное событие от устройства |

### Различение событий и ответов

```python
eventCode = struct.unpack('<H', data[0:2])
if eventCode == 128:
    # Это ответ на команду, result code в data[10]
else:
    # Это событие (heartbeat / print done / power on)
```

---

## Реализация на ESP32

### Общий план

1. Инициализировать Zigbee-стек как **координатор**
2. Настроить кастомный профиль `0xC000`
3. Зарегистрировать endpoint 1 с кластерами `[0x0000, 0xFE00]`
4. Сформировать сеть на одном из каналов [11, 14, 15, 19, 20, 24, 25]
5. Разрешить присоединение (`permit joining`)
6. Дождаться присоединения принтера (запомнить EUI64)
7. Настроить шифрование (link key)
8. Принимать события от принтера
9. Отправлять изображения блоками по 512 байт

### Формирование ZCL-фрейма

```c
uint8_t frame[5 + 1 + 512]; // макс. размер
frame[0] = 0x05;             // Frame Control: cluster-specific + mfg-specific
frame[1] = 0x02;             // Manufacturer Code low byte
frame[2] = 0x10;             // Manufacturer Code high byte
frame[3] = seq_number++;     // Sequence number
frame[4] = 0x01;             // Command ID = 1
frame[5] = block_id;         // Block ID (0-255, big-endian)
memcpy(&frame[6], image_data + offset, chunk_size); // до 512 байт
```

### Обработка ответа

```c
void on_message_received(uint8_t *data, uint16_t len) {
    uint16_t event_code = data[0] | (data[1] << 8); // little-endian
    
    if (event_code == 0x0080) {
        uint8_t result = data[10];
        // result == 0 → блок принят, отправляем следующий
    } else if (event_code == 0x0001) {
        // heartbeat — принтер жив
    } else if (event_code == 0x0002) {
        // печать завершена
    } else if (event_code == 0x0003) {
        // принтер включился
    }
}
```

### Алгоритм отправки изображения

```
1. Подготовить бинарные данные изображения (384×N пикселей, 1bpp)
2. block_id = 0
3. Для каждого блока (512 байт):
   a. Сформировать ZCL-фрейм с block_id + данные
   b. Отправить unicast на Node ID принтера
   c. Ждать подтверждения (до 5 сек)
   d. Если ошибка — повторить (до 4 раз, пауза 1 сек)
   e. block_id = (block_id >= 255) ? 1 : block_id + 1
4. Дождаться EVENT_DID_PRINT (код 2)
```

---

## Выбор Zigbee-чипа/модуля

### Вариант 1: ESP32-H2 (рекомендуется)

Нативная поддержка IEEE 802.15.4, встроенный Zigbee-стек.

| Параметр | Значение |
|----------|----------|
| Чип | ESP32-H2 |
| Модули | ESP32-H2-MINI-1, ESP32-H2-WROOM |
| 802.15.4 | Да (нативно) |
| Zigbee SDK | esp-zigbee-sdk (Espressif) |
| Роль координатора | Да |
| Кастомные профили | Да (через raw ZCL API) |
| Wi-Fi | **Нет** (нужен отдельный ESP32 для Wi-Fi) |
| BLE | Да |

**Плюсы**: всё в одном чипе, нативная поддержка, хорошая документация от Espressif.

**Минусы**: нет Wi-Fi — если нужен веб-интерфейс, потребуется второй чип (ESP32-C3/S3) через UART/SPI.

### Вариант 2: ESP32-C6 (лучший вариант для всё-в-одном)

Wi-Fi 6 + BLE 5 + IEEE 802.15.4 в одном чипе.

| Параметр | Значение |
|----------|----------|
| Чип | ESP32-C6 |
| Модули | ESP32-C6-MINI-1, ESP32-C6-WROOM-1 |
| 802.15.4 | Да (нативно) |
| Wi-Fi | Да (Wi-Fi 6) |
| Zigbee SDK | esp-zigbee-sdk |
| Роль координатора | Да |

**Плюсы**: Wi-Fi + Zigbee в одном чипе, можно сделать веб-интерфейс.

**Минусы**: RISC-V одноядерный, меньше производительности чем ESP32-S3.

### Вариант 3: ESP32 + внешний Zigbee NCP (UART)

Классический ESP32 (S3/C3) + внешний Zigbee-чип через UART.

#### Подходящие NCP-модули:

| Модуль | Чип | Интерфейс | Протокол | Примечание |
|--------|-----|-----------|----------|------------|
| **EFR32MG21** | Silicon Labs | UART | EZSP | Тот же протокол что в оригинале! |
| **EFR32MG24** | Silicon Labs | UART | EZSP | Новее, лучше |
| **SONOFF ZBDongle-E** | EFR32MG21 | USB-UART | EZSP | Готовый USB-стик |
| **SONOFF ZBDongle-P** | TI CC2652P | USB-UART | Z-Stack | Альтернативный стек |
| **TI CC2652R** | Texas Instruments | UART | Z-Stack | Популярный, мощный |
| **TI CC2652P** | TI | UART | Z-Stack | +20dBm PA |
| **Ebyte E72-2G4M20S1E** | TI CC2652P | UART | Z-Stack | Модуль для пайки |
| **Ebyte E180-ZG120B** | EFR32MG1B | UART | EZSP | Компактный модуль |

**Плюсы**: полная мощность ESP32 (два ядра, Wi-Fi, BLE), проверенные Zigbee-чипы.

**Минусы**: два чипа, сложнее схема, нужен UART-мост.

### Рекомендация

| Сценарий | Рекомендация |
|----------|-------------|
| Минимум компонентов, без Wi-Fi | **ESP32-H2** |
| Всё-в-одном с веб-интерфейсом | **ESP32-C6** |
| Максимальная совместимость с оригиналом | **ESP32 + EFR32MG21 (EZSP)** |
| Быстрый старт, готовое решение | **ESP32 + SONOFF ZBDongle-E** |
| Лучший радиус действия | **ESP32 + CC2652P (+20dBm)** |

### Важно про EZSP vs Z-Stack

- **EZSP** (Silicon Labs) — тот же протокол что в оригинальном бридже. Можно почти 1:1 портировать логику из декомпилированного кода.
- **Z-Stack** (Texas Instruments) — другой стек, но Zigbee-совместимый. Нужно адаптировать API-вызовы, но ZCL-фреймы идентичны.
- **esp-zigbee-sdk** (Espressif для H2/C6) — обёртка вокруг ZBOSS стека. Поддерживает кастомные профили и кластеры через raw API.

---

## Ключевые файлы

| Файл | Описание |
|------|----------|
| `api.pyc.py` | Zigbee API: формирование сети, отправка блоков, обработка ответов |
| `framework.pyc.py` | Application Framework: ZCL-парсинг, маршрутизация сообщений, управление стеком |
| `weminuche_bridge.pyc.py` | Главный демон: инициализация, WebSocket-клиент, очереди команд |
| `trust_center.pyc.py` | Trust Center: генерация ключей, ротация, управление link keys |
| `berg_cloud_socket_api.pyc.py` | WebSocket-клиент к Berg Cloud (SSL + клиентские сертификаты) |
| `device_command.pyc.py` | Модель команды: парсинг JSON, хранение payload, коды ответов |
| `device_event.pyc.py` | Модель события: heartbeat, print done, power on |
| `ezsp.pyc.py` | EZSP протокол: SPI-связь с NCP, все низкоуровневые команды |
| `byte_tuple.pyc.py` | Утилиты: конвертация EUI64, extended PAN ID, ключей |
| `security_config.pyc.py` | Константы профилей безопасности |
| `zcl.pyc.py` | ZCL константы: ID кластеров, команд, статусов |
| `BERGCloudConst.pyc.py` | Константы протокола Berg Cloud (команды, события) |
| `fragmentation.pyc.py` | APS-фрагментация для пакетов > 82 байт |
| `form_and_join.pyc.py` | Сканирование каналов, поиск PAN ID, формирование сети |

---

---

## Генерация Link Key из Claim Code

Алгоритм восстановлен из серверного кода [Sirius](https://github.com/nordprojects/sirius) (`sirius/coding/claiming.py`).

### Claim Code

Claim code — это 16-символьная строка в кастомном base32, напечатанная на наклейке каждого принтера. Формат: `xxxx-xxxx-xxxx-xxxx` (дефисы декоративные).

### Структура Claim Code (80 бит)

```
┌──────────────────┬────────────────────────┬──────────────────┐
│  CRC (16 бит)    │   Secret (40 бит)      │ hardware_xor     │
│                  │                        │   (24 бита)      │
└──────────────────┴────────────────────────┴──────────────────┘
  MSB ←───────────────── 80 бит ───────────────────→ LSB
```

- **hardware_xor** (24 бита) — детерминированный хеш EUI64 устройства
- **secret** (40 бит) — случайный секрет, уникальный для принтера
- **CRC** (16 бит) — CRC16 от остальных 64 бит (для защиты от опечаток)

### Hardware XOR из EUI64

Lossy-хеш: 8 байт EUI64 сжимаются в 3 байта (24 бита):

```python
def hardware_xor_from_device_address(device_address):
    b = bytearray.fromhex(device_address)  # "000d6f000273ce0b"
    b.reverse()                             # little-endian

    claim_address = bytearray(3)
    claim_address[0] = b[0] ^ b[5]
    claim_address[1] = b[1] ^ b[3] ^ b[6]
    claim_address[2] = b[2] ^ b[4] ^ b[7]

    return claim_address[2] << 16 | claim_address[1] << 8 | claim_address[0]
```

### Генерация Link Key

```python
CLAIM_CODE_SALT = bytes([
    0x38, 0x96, 0x10, 0xd9, 0xb6, 0xb1, 0x0d, 0x16,
    0x9e, 0xe9, 0xbf, 0x87, 0x95, 0x32, 0x62, 0x5b
])

def generate_link_key(secret_5_bytes):
    # Паддинг до 16 байт (Matyas-Meyer-Oseas style)
    input_length = len(secret_5_bytes) + len(CLAIM_CODE_SALT)
    padded = secret_5_bytes + b'\x80' + b'\x00' * 8
    padded += bytes([(input_length * 8) >> 8 & 0xff])
    padded += bytes([(input_length * 8) & 0xff])

    # Два раунда AES-ECB: сначала соль, потом западдированный secret
    output = bytes(16)
    for block in [CLAIM_CODE_SALT, padded]:
        h = AES.new(output, AES.MODE_ECB).encrypt(block)
        output = bytes([h[i] ^ block[i] for i in range(16)])

    return output  # 16 байт — это AES-128 link key
```

### Полная цепочка: Claim Code → Link Key

```
Claim Code: "5oop-e9dp-hh7v-fjqo"
    │
    ▼ Убрать дефисы, base32 decode
80 бит: hardware_xor(24) + secret(40) + crc(16)
    │
    ▼ CRC16 проверка
    │
    ▼ Извлечь secret (40 бит → 5 байт, little-endian)
    │
    ▼ generate_link_key(secret_5_bytes)
    │
    ▼ AES-ECB(salt + padded_secret)
    │
Link Key: 16 байт → Base64 → отправить бриджу
```

### Base32 алфавит (кастомный)

Отличия от стандартного base32:
- Буква **A** пропущена (не используется)
- **I** → **1**, **L** → **1** (защита от опечаток)
- **U** → **V** (защита от опечаток)

```
0123456789BCDEFGHJKMNOPQRSTVWXYZ
```

### Для ESP32

Если у тебя есть claim code с наклейки принтера, ты можешь один раз вычислить link key и захардкодить его в прошивку. Алгоритм полностью детерминирован, облако не нужно.

---

## Бинарный payload команды печати

Данные, которые бридж отправляет принтеру через Zigbee, имеют определённую структуру поверх сырых пиксельных данных.

### Общая структура (из Sirius `encoders.py`)

```
┌─────────────────────────────────────────────────┐
│               Command Header (12 байт)          │
├──────┬──────┬───────────┬──────────┬─────────────┤
│ DevT │ Res  │  Command  │ print_id │   CRC       │
│ 1B   │ 1B   │  2B (LE)  │ 4B (LE)  │  4B (LE)    │
│ 0x01 │ 0x00 │  0x0001   │  <id>    │  0x00000000 │
└──────┴──────┴───────────┴──────────┴─────────────┘
│           Payload Length (4 байта LE)            │
├──────────────────────────────────────────────────┤
│                 Payload                          │
│  ┌────────────────────────────────────────────┐  │
│  │  total_size (4B LE) + reserved (1B)        │  │
│  │  Header Region:                            │  │
│  │    type (1B) + header_len (4B LE)          │  │
│  │    Printer Control (13 байт)               │  │
│  │    Printer Data Command (8 байт)           │  │
│  │  RLE Image Data:                           │  │
│  │    type=0x01 (1B) + rle_len (4B LE)        │  │
│  │    <RLE-encoded pixels>                    │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### Device Type

| Значение | Устройство |
|----------|-----------|
| 0x01 | Little Printer |

### Printer Control Bytes

Управление термоголовкой (13 байт):

```
0x1d 0x73 0x03 0xe8   — макс. скорость печати (1000)
0x1d 0x61 0xd0         — ускорение (208)
0x1d 0x2f 0x0f         — пиковый ток (15)
0x1d 0x44 0x80         — макс. интенсивность (128)
```

### Printer Data Command

Команда начала растровых данных (8 байт):

```
0x1b 0x2a <n1> <n2> <n3> 0x00 0x00 0x30
```

Где `n1`, `n2`, `n3` — размер данных в байтах (pixel_count / 8), закодированный как:
- `n3` = размер / 65536
- `n2` = (размер % 65536) / 256
- `n1` = размер % 256

---

## RLE-кодирование изображений

Принтер принимает не сырой bitmap, а **RLE-сжатое** изображение.

### Подготовка изображения

1. Исходное изображение (HTML или PNG)
2. Обрезка до ширины **384 пикселя**, макс. высота 10000 px
3. Конвертация в **1-bit** (чёрно-белый)
4. **Поворот на 180°** (принтер печатает снизу вверх)
5. RLE-кодирование

### Алгоритм RLE

Пиксели группируются в «пробеги» одного цвета, чередуя белый и чёрный. **Первый пробег всегда белый** (если изображение начинается с чёрного, добавляется нулевой белый пробег).

Кодирование длин пробегов:

| Длина пробега | Кодирование |
|---------------|-------------|
| 0–251 | 1 байт = длина |
| 252 | Escape: пробег = 384 пикселей |
| 253 | Escape: пробег = 768 пикселей |
| 254 | Escape: пробег = 1152 пикселей |
| 255 | Escape: пробег = 1536 пикселей |

Для длин > 251 — разбивка на куски (сначала большие, затем остаток). Каждый кусок кроме первого предваряется нулевым байтом (переключение цвета обратно).

### Формат RLE-данных

```
┌──────────┬────────────────┬─────────────────────┐
│ Type=0x01│ compressed_len │ RLE bytes...        │
│  1 byte  │   4 bytes LE   │ variable            │
└──────────┴────────────────┴─────────────────────┘
```

### Пример кодирования

```
Пиксели:  WWWWWBBBBBBWWW  (W=белый, B=чёрный)
Пробеги:  белый=5, чёрный=6, белый=3
RLE:      [0x05, 0x06, 0x03]
```

---

## Команды принтера

### Коды команд (из Sirius `protocol.proto`)

| Код | Hex | Команда | Описание |
|-----|-----|---------|----------|
| 1 | 0x0001 | `set_delivery_and_print` | Напечатать с лицом (face) |
| 2 | 0x0002 | `set_delivery` | Сохранить, но не печатать |
| 17 | 0x0011 | `set_delivery_and_print_no_face` | Напечатать без лица |
| 18 | 0x0012 | `set_delivery_no_face` | Сохранить без лица |
| 258 | 0x0102 | `set_personality` | Установить «личность» (4 изображения: face, nothing_to_print, no_bridge, no_internet) |
| 257 | 0x0101 | `set_personality_with_message` | Личность + приветственное сообщение (5 изображений) |
| 514 | 0x0202 | `set_quip` | Установить «quip» (3 изображения-шутки) |
| 61440 | 0xF000 | `firmware_update` | Обновление прошивки |

### Payload для разных команд

| Команда | Payload |
|---------|---------|
| `set_delivery_and_print` | 1 × RLE image |
| `set_personality` | 4 × RLE image (face + no_print + no_bridge + no_internet) |
| `set_personality_with_message` | 5 × RLE image (те же + message) |
| `set_quip` | 3 × RLE image |

Для команд с несколькими изображениями payload — конкатенация нескольких `_encode_pixels()` блоков.

### BERGCloud константы

| Константа | Hex | Описание |
|-----------|-----|----------|
| `BC_COMMAND_DISPLAY_IMAGE` | `0xD000` | Отобразить изображение |
| `BC_COMMAND_DISPLAY_TEXT` | `0xD001` | Отобразить текст |
| `BC_COMMAND_START_BINARY` | `0xC000` | Начало бинарной передачи |
| `BC_COMMAND_SET_BERGCLOUD_ID` | `0xB000` | Установить Berg Cloud ID |
| `BC_EVENT_PRODUCT_ANNOUNCE` | `0xA000` | Анонс продукта |
| `BC_COMMAND_FIRMWARE_ARDUINO` | `0xF010` | Прошивка Arduino |
| `BC_COMMAND_FIRMWARE_MBED` | `0xF020` | Прошивка mbed |

---

## WebSocket JSON-протокол (Bridge ↔ Server)

Полная спецификация протокола между бриджем и сервером, восстановленная из обоих источников.

### События (Bridge → Server)

#### PowerOn (первое сообщение после подключения)

```json
{
  "type": "BridgeEvent",
  "bridge_address": "000d6f0002ff7a91",
  "timestamp": 1426256447.70695,
  "json_payload": {
    "name": "power_on",
    "model": "A",
    "firmware_version": "v2.3.1-f3c7946",
    "ncp_version": "0x46C5",
    "local_ip_address": "192.168.2.117",
    "mac_address": "40:d8:55:19:77:2e",
    "uptime": "830.55 798.31",
    "uboot_environment": "<base64>",
    "network_info": {
      "node_type": "EMBER_COORDINATOR",
      "security_level": 5,
      "security_profile": "Custom",
      "network_status": "EMBER_JOINED_NETWORK",
      "pan_id": "0xDCC9",
      "node_eui64": "0x000d6f0002ff7a91",
      "power": 8,
      "node_id": "0x0000",
      "channel": 16,
      "radio_power_mode": "EMBER_TX_POWER_MODE_BOOST",
      "extended_pan_id": "0x42455247b439420c"
    }
  }
}
```

#### DeviceConnect

```json
{
  "type": "BridgeEvent",
  "bridge_address": "000d6f0002ff7a91",
  "json_payload": {
    "name": "device_connect",
    "device_address": "000d6f000273ce0b"
  }
}
```

#### EncryptionKeyRequired

```json
{
  "type": "BridgeEvent",
  "bridge_address": "000d6f0002ff7a91",
  "json_payload": {
    "name": "encryption_key_required",
    "device_address": "000d6f000273ce0b"
  }
}
```

#### DeviceEvent (бинарный payload в base64)

```json
{
  "type": "DeviceEvent",
  "bridge_address": "000d6f0002ff7a91",
  "device_address": "000d6f000273ce0b",
  "binary_payload": "AQAAAAAABAAAABQAAAA=",
  "timestamp": 1346501618.506583,
  "rssi_stats": [-31, -32, -30]
}
```

### Команды (Server → Bridge)

#### AddDeviceEncryptionKey

```json
{
  "type": "BridgeCommand",
  "bridge_address": "000d6f0002ff7a91",
  "command_id": 42,
  "timestamp": "0",
  "json_payload": {
    "name": "add_device_encryption_key",
    "params": {
      "device_address": "000d6f000273ce0b",
      "encryption_key": "dGhpcyBpcyBhIGtleQ=="
    }
  }
}
```

#### DeviceCommand (печать)

```json
{
  "type": "DeviceCommand",
  "bridge_address": "000d6f0002ff7a91",
  "command_id": 123,
  "device_address": "000d6f000273ce0b",
  "binary_payload": "<base64 encoded printer payload>",
  "timestamp": "0"
}
```

#### Другие BridgeCommand

| name | params | Описание |
|------|--------|----------|
| `add_device_encryption_key` | device_address, encryption_key | Добавить link key |
| `set_cloud_log_level` | level (string/int) | Установить уровень логирования |
| `leave` | — | Покинуть Zigbee-сеть |
| `form` | channels (list) | Создать новую сеть |
| `pjoin` | duration (int) | Разрешить присоединение |
| `restart` | — | Перезапуск демона |
| `reboot` | — | Перезагрузка устройства |

### Ответы (Bridge → Server)

```json
{
  "type": "DeviceCommandResponse",
  "bridge_address": "000d6f0002ff7a91",
  "device_address": "000d6f000273ce0b",
  "command_id": 123,
  "return_code": 0,
  "rssi_stats": [-31, -32],
  "transfer_time": 2.45,
  "timestamp": 1346501620.0
}
```

---

## Структура бинарных событий от принтера

Все бинарные события (DeviceEvent.binary_payload после base64-декодирования) имеют общий заголовок:

### Заголовок (10 байт)

```
┌───────────────┬───────────────┬──────────────────┐
│  Event Code   │  Command ID   │  Payload Length  │
│  2 bytes LE   │  4 bytes LE   │  4 bytes LE      │
└───────────────┴───────────────┴──────────────────┘
```

### EVENT_HEARTBEAT (code = 0x0001)

Payload: 4 байта — uptime принтера (uint32 LE, секунды).

### EVENT_DID_PRINT (code = 0x0002)

Payload: 5 байт:

```
┌─────────────┬──────────────┐
│ print_type  │  print_id    │
│   1 byte    │  4 bytes LE  │
└─────────────┴──────────────┘
```

| print_type | Значение |
|------------|----------|
| 0x01 | delivery (обычная печать) |
| 0x10 | nothing_to_print (нечего печатать) |
| 0x11 | quip (шутка) |

### EVENT_DID_POWER_ON (code = 0x0003)

Payload: 58 или 74 байта (с/без фрагментации):

```
┌──────────┬─────────────────────┬─────────────────────┬─────────────┬──────────────────┐
│ DevType  │ firmware_build_ver  │ loader_build_ver    │ proto_ver   │ reset_desc       │
│ 4B LE    │ 24/32 bytes         │ 24/32 bytes         │ 4B LE       │ 2B LE            │
└──────────┴─────────────────────┴─────────────────────┴─────────────┴──────────────────┘
```

Коды сброса (старший байт `reset_desc`):

| Код | Описание |
|-----|----------|
| 0x0000 | Неизвестная причина |
| 0x0100 | FIB bootloader |
| 0x0200 | Ember bootloader |
| 0x0300 | Внешний reset |
| 0x0400 | Power on (включение питания) |
| 0x0500 | Watchdog |
| 0x0600 | Программный |
| 0x0700 | Software crash |
| 0x0800 | Flash failure |
| 0x0900 | Fatal error |
| 0x0A00 | Access fault |

### BC_EVENT_PRODUCT_ANNOUNCE (code = 0xA000)

Payload: 20 байт — product_id (16 байт, big-endian) + version (4 байта).

---

## Формат данных для печати

### Изображение

Принтер Little Printer печатает растровые изображения:
- Ширина: **384 пикселя** (48 байт на строку, 1 бит на пиксель)
- Высота: до **10000 пикселей**
- Формат: 1bpp, чёрно-белый, RLE-сжатие
- Изображение **переворачивается на 180°** перед отправкой
- Первый пиксель должен быть **белым** (иначе принтер инвертирует)

### Конвейер подготовки (из Sirius)

```
HTML
  → Jinja2 template (ширина 384px, шрифт Helvetica/Arial 30px)
  → PhantomJS/Selenium рендер (окно 384×5 px, скриншот в PNG)
  → Обрезка до 384px ширины
  → Конвертация в 1-bit (чёрно-белый)
  → Поворот 180°
  → RLE-кодирование
  → Добавление printer control bytes
  → Обёртка в command header (device_type + command + print_id)
  → Base64 → JSON → WebSocket → Bridge → Zigbee blocks
```

---

## Полная последовательность для ESP32

```
1. Инициализация
   ├── Инициализировать Zigbee-стек
   ├── Настроить как координатор
   ├── Зарегистрировать endpoint 1 (profile=0xC000, clusters=[0x0000, 0xFE00])
   ├── Настроить безопасность (Security Level 5, случайный network key)
   └── Выбрать канал (energy scan → минимальный шум)

2. Формирование сети
   ├── Сканировать PAN ID (найти свободный)
   ├── Сформировать сеть (Extended PAN ID, PAN ID, канал)
   └── Разрешить присоединение (pjoin 255)

3. Подключение принтера
   ├── Принтер ищет сеть → присоединяется
   ├── Trust Center Handler: получить EUI64 принтера
   ├── Добавить link key (если нужен)
   └── Дождаться EVENT_DID_POWER_ON от принтера

4. Печать
   ├── Подготовить изображение (384px wide, 1bpp)
   ├── Найти Node ID по EUI64: emberLookupNodeIdByEui64()
   ├── Нарезать на блоки по 512 байт
   ├── Для каждого блока:
   │   ├── Сформировать ZCL-фрейм (frame_ctl=0x05, mfg=0x1002, cmd=1)
   │   ├── Payload = blockID (1 byte, big-endian) + data (≤512 bytes)
   │   ├── Отправить unicast (APS fragmentation для пакетов >82 байт)
   │   ├── Ждать ACK + response (до 5 сек)
   │   └── При ошибке: retry до 4 раз, пауза 1 сек
   └── Дождаться EVENT_DID_PRINT (код 2)
```

---

## Ключевые файлы

### Декомпилированный Bridge (`berg-bridge-dump/DECOMPILED/`)

| Файл | Описание |
|------|----------|
| `api.pyc.py` | Zigbee API: формирование сети, отправка блоков, обработка ответов |
| `framework.pyc.py` | Application Framework: ZCL-парсинг, маршрутизация сообщений, управление стеком |
| `weminuche_bridge.pyc.py` | Главный демон: инициализация, WebSocket-клиент, очереди команд |
| `trust_center.pyc.py` | Trust Center: генерация ключей, ротация, управление link keys |
| `berg_cloud_socket_api.pyc.py` | WebSocket-клиент к Berg Cloud (SSL + клиентские сертификаты) |
| `device_command.pyc.py` | Модель команды: парсинг JSON, хранение payload, коды ответов |
| `device_event.pyc.py` | Модель события: heartbeat, print done, power on |
| `ezsp.pyc.py` | EZSP протокол: SPI-связь с NCP, все низкоуровневые команды |
| `byte_tuple.pyc.py` | Утилиты: конвертация EUI64, extended PAN ID, ключей |
| `security_config.pyc.py` | Константы профилей безопасности |
| `zcl.pyc.py` | ZCL константы: ID кластеров, команд, статусов |
| `BERGCloudConst.pyc.py` | Константы протокола Berg Cloud (команды, события) |
| `fragmentation.pyc.py` | APS-фрагментация для пакетов > 82 байт |
| `form_and_join.pyc.py` | Сканирование каналов, поиск PAN ID, формирование сети |

### Сервер Sirius (`sirius/`)

| Файл | Описание |
|------|----------|
| `sirius/protocol/protocol_loop.py` | Основной цикл: WebSocket accept, send_message, маршрутизация |
| `sirius/protocol/messages.py` | Все типы сообщений (namedtuple): PowerOn, DeviceCommand и т.д. |
| `sirius/coding/encoders.py` | Кодирование команд: RLE → printer payload → JSON |
| `sirius/coding/decoders.py` | Декодирование событий: JSON → binary → типизированные сообщения |
| `sirius/coding/image_encoding.py` | HTML/PNG → 1bit → RLE кодирование |
| `sirius/coding/claiming.py` | Claim code → link key (AES-ECB с солью) |
| `sirius/coding/bitshuffle.py` | EUI64 → hardware_xor (3-байтный хеш) |
| `sirius/coding/crc16.py` | CRC16 для проверки claim code |
| `sirius/models/hardware.py` | Модели Bridge, Printer, ClaimCode (SQLAlchemy) |
| `sirius/web/webapp.py` | Flask-приложение: WebSocket endpoint, веб-интерфейс |
| `notes/protocol.proto` | Protobuf-описание протокола (справочное) |

---

## Ссылки и ресурсы

- [Sirius](https://github.com/nordprojects/sirius) — Альтернативный сервер Little Printer (Nord Projects), основной источник по протоколу
- [littleprinter.nordprojects.co](http://littleprinter.nordprojects.co) — Публичный инстанс сервера Sirius
- [esp-zigbee-sdk](https://github.com/espressif/esp-zigbee-sdk) — Zigbee SDK для ESP32-H2/C6
- [ZBOSS](https://developer.nordicsemi.com/nRF_Connect_SDK/doc/zboss_api_doc/index.html) — Стек ZBOSS (используется в esp-zigbee-sdk)
- [Silicon Labs EZSP Reference](https://www.silabs.com/documents/public/user-guides/ug100-ezsp-reference-guide.pdf) — Документация EZSP
- [Zigbee Cluster Library (ZCL)](https://zigbeealliance.org/developer_resources/) — Спецификация ZCL
