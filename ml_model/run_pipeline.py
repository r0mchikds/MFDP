import os
import shutil
import time
from datetime import datetime
import papermill as pm
import argparse


log_path = "pipeline_log.txt"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"[{timestamp}] {msg}"
    print(full_msg)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

# Аргументы командной строки
parser = argparse.ArgumentParser()
parser.add_argument("--skip-cleanup", action="store_true", help="Не очищать папку data/")
parser.add_argument("--clean-only", action="store_true", help="Только очистка папки data/, без запуска ноутбуков")
parser.add_argument("--only", type=str, help="Выполнить только указанный ноутбук")
parser.add_argument("--up-to", type=str, help="Выполнить все ноутбуки ДО этого включительно")
parser.add_argument("--from_", dest="from_nb", type=str, help="Выполнить все ноутбуки НАЧИНАЯ с этого")
args = parser.parse_args()

# Очистка папки data
if not args.skip_cleanup or args.clean_only:
    data_dir = "data"
    log("🧹 Cleaning up data/ directory...")
    for file in os.listdir(data_dir):
        path = os.path.join(data_dir, file)
        if file.endswith(".csv") and os.path.isfile(path):
            os.remove(path)
        elif file == "images" and os.path.isdir(path):
            shutil.rmtree(path)
    log("✅ Data folder cleaned.\n")
else:
    log("⏭️ Пропуск очистки папки data/ (--skip-cleanup)\n")

# Если указано только очищать — завершаем
if args.clean_only:
    log("🧺 Очистка завершена. Ноутбуки не запускались (--clean-only).")
    exit(0)

# Список ноутбуков
notebooks = [
    "01_amazon_grocery_preprocessing_and_eda.ipynb",
    "02_amazon_grocery_interactions_preprocessing_and_eda.ipynb",
    "03_amazon_dataset_train_test_generation.ipynb",
    "04_model_training_and_evaluation.ipynb",
    "05_amazon_dataset_train_test_generation_rating_based.ipynb",
    "06_model_training_and_evaluation_rating_based.ipynb"
]

if args.only:
    notebooks = [args.only]
elif args.up_to:
    if args.up_to in notebooks:
        notebooks = notebooks[:notebooks.index(args.up_to) + 1]
    else:
        log(f"❌ Указанный ноутбук {args.up_to} не найден в списке.")
        exit(1)
elif args.from_nb:
    if args.from_nb in notebooks:
        notebooks = notebooks[notebooks.index(args.from_nb):]
    else:
        log(f"❌ Указанный ноутбук {args.from_nb} не найден в списке.")
        exit(1)

# Прогон каждого ноутбука
for nb in notebooks:
    log(f"🚀 START: {nb}")
    start = time.time()

    pm.execute_notebook(
        input_path=nb,
        output_path=nb,
        kernel_name="python3"
    )

    duration = time.time() - start
    log(f"✅ DONE: {nb} (⏱️ {duration:.1f} sec)\n")
