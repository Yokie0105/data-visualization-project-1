files=("pigplot.py" "network.py" "spiral.py")

for file in "${files[@]}"; do
  without_extension="${file%.*}"
  marimo export html-wasm "$file" -o apps/"$without_extension".html --mode run
done
