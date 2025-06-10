# MLOps Team-21 — Titanic Survival Prediction API

FastAPI-сервис, который по пассажирским данным предсказывает, выжил человек или нет.  
Код организован по принципам **MLOps**: данные и модели версионируются в [DVC], пайплайн обучения описан в `src/services/model_pipeline`, а сборка/тесты/деплой проходят автоматически в **Jenkins**.

---

## 📋 Requirements

| Что нужно | Зачем | Где взять / как задать |
|-----------|-------|------------------------|
| **Python 3.11** | локальный запуск и тесты | <https://www.python.org> |
| **Docker 24+** | сборка контейнера | <https://docs.docker.com/engine/install> |
| **service_account.json** | сервис-аккаунт GDrive, даёт DVC доступ к датасетам и моделям | создайте в Google Cloud → IAM & Admin → Service Accounts → *Keys ► JSON* |
| **Git LFS** | если захотите пушить большие файлы | <https://git-lfs.com> |

> 🔑 **Ключ сервис-аккаунта**
> Для CI и local-launch в примерах ниже путь передаётся через переменную
> `DVC_REMOTE_GDRIVE_GDRIVE_SERVICE_ACCOUNT_JSON_FILE_PATH`.

---

## 🖥 Local setup & run

```bash
git clone https://github.com/your-org/MLOps_team21_final.git
cd MLOps_team21_final

# 1. Python venv
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .          # делает пакет src/ импортируемым

# 2. DVC — тянем данные и модель
export DVC_REMOTE_GDRIVE_GDRIVE_USE_SERVICE_ACCOUNT=true
export DVC_REMOTE_GDRIVE_GDRIVE_SERVICE_ACCOUNT_JSON_FILE_PATH="$(pwd)/service_account.json"
dvc pull                   # ~200 MB

# 3. Проверяем всё
black --check src tests
mypy src tests
pytest -q

# 4. Запускаем API
uvicorn src:app --reload
# →  http://127.0.0.1:8000/docs 
```

---

## 🐳 Docker build & run

# 1. Собираем образ team21/model:latest
```bash
docker build -t team21/model:latest .
```

# 2. Передаём в контейнер ключ SA (+порт)
```bash
docker run -d -p 8000:8000 \
  -e DVC_REMOTE_GDRIVE_GDRIVE_USE_SERVICE_ACCOUNT=true \
  -e DVC_REMOTE_GDRIVE_GDRIVE_SERVICE_ACCOUNT_JSON_FILE_PATH=/run/secrets/gdrive_sa.json \
  --secret id=gdrive_sa.json,src=./service_account.json \
  team21/model:latest
```

## 🛠 CI/CD (Jenkins)

* Pipeline-скрипт: **Jenkinsfile**
* Тесты + линт + обучение + docker build + push → Docker Hub
* Данные `dvc pull` аутентифицируются через Secret-file `service_account.json`.
* Учётка Docker Hub хранится в **Credentials** с ID `docker-credentials`.

Скриншоты хранятся в папке **docs/**:

| Этап          | Скрин                                          |
| ------------- | ---------------------------------------------- |
| Успешный билд | ![Build green](docs/jenkins_build_success.png) |
| Граф Pipeline | ![Pipeline view](docs/jenkins_pipeline.png)    |
| Пуш образа    | ![Push log](docs/jenkins_docker_push.png)      |

---

## 📂 Project structure

```
├── src/                     # приложение + ML-код
│   ├── __init__.py          # экспорт app
│   └── services/
│       ├── model_pipeline/  # train, preprocess, tests
│       └── ...
├── tests/                   # pytest suites
├── data/                    # DVC-tracked datasets
├── models/                  # DVC-tracked artefacts
├── Dockerfile
├── Jenkinsfile
└── README.md
```

---

## ✨ Result

| Metric           | Value                               |
| ---------------- | ----------------------------------- |
| **mypy**         | 0 errors                            |
| **black**        | 100 % formatted                     |
| **pytest**       | 27 passed                           |
| **Docker image** | `docker.io/team21/model:⟨build-id⟩` |