for f in *.pyc; do
  uncompyler.py ./"$f" > ./"${f%}.py"
done
