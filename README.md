# awesome-school-coding-test

어썸스쿨 사전 과제

## 디렉토리 구조

```
.
├── server/   # Django REST Framework (API 서버)
└── web/      # 프론트엔드 HTML / CSS / JS
```

`web/`은 nginx·CDN이 직접 서빙하며 Django를 경유하지 않습니다.
아래 명령은 모두 `server/` 디렉토리에서 실행합니다.

## 요구사항

- Python 3.14 (`.python-version` 참고)
- [uv](https://docs.astral.sh/uv/) — 패키지 / 가상환경 관리
- PostgreSQL 15 이상

## 설치

### 1. 의존성 설치

```bash
cd server
uv sync
```

`.venv/`가 생성되고 `uv.lock`에 고정된 버전으로 설치됩니다.

### 2. 환경 변수 설정

`.env.example`을 복사해 `.env`를 만들고 값을 채워주세요.

```bash
cp .env.example .env
```

```dotenv
# Django
DJANGO_SECRET_KEY=

# Database (PostgreSQL)
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

시크릿 키는 아래 명령으로 생성할 수 있습니다.

> ```bash
> uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

`.env`는 `local` / `testing` 환경에서만 `python-dotenv`로 자동 로드됩니다.
`dev` / `prod`는 서버의 실제 환경 변수를 사용하므로 `.env`를 읽지 않습니다.

### 3. 마이그레이션

```bash
uv run python manage.py migrate --settings=config.settings.local
```

### 4. 개발 서버 실행

```bash
uv run python manage.py runserver --settings=config.settings.local
```

http://127.0.0.1:8000 에서 확인하실 수 있습니다.

`--settings`에 들어갈 값은 실행 환경에 따라 달라집니다. 선택지는 아래 [설정 환경](#설정-환경-settings) 섹션을 참고해주세요.

## 테스트

```bash
uv run python manage.py test --settings=config.settings.testing
```

테스트 실행 시 Django가 테스트용 데이터베이스를 자동으로 생성하고, 끝나면 삭제합니다.
`.env`에 지정한 데이터베이스는 그대로 유지됩니다.

## 코드 스타일

[ruff](https://docs.astral.sh/ruff/)로 문자열 따옴표 스타일을 검사합니다. 이중따옴표(`"`)로 통일합니다.

```bash
uv run ruff check .         # 검사
uv run ruff check --fix .   # 자동 수정
```

적용 규칙은 `pyproject.toml`의 `[tool.ruff.lint]`에 정의되어 있습니다.

## 설정 환경 (settings)

설정은 `config/settings/` 아래에 환경별로 분리되어 있으며, 모두 `base.py`를 상속합니다.

| 모듈 | 용도 | `.env` 로드 |
| --- | --- | --- |
| `config.settings.local` | 개발자가 직접 노트북/PC에서 개발할 때 | O |
| `config.settings.testing` | unittest 실행 시 | O |
| `config.settings.dev` | 개발 서버 | X |
| `config.settings.prod` | 프로덕션 서버 | X |

`manage.py`의 기본값이 `config.settings.local`이므로 로컬 개발 시에는 별도로 지정하지 않아도 됩니다.
다른 환경으로 실행할 때는 `--settings` 옵션이나 `DJANGO_SETTINGS_MODULE` 환경 변수를 사용합니다.

```bash
uv run python manage.py runserver --settings=config.settings.dev
```

## 참고

- 데이터베이스는 PostgreSQL을 사용하며, `local` / `dev` / `prod` / `testing` 모두 동일합니다.
- 정적 파일 책임은 아래와 같이 나뉩니다.

  | 대상 | 서빙 주체 |
  | --- | --- |
  | `web/` (프론트엔드) | nginx / CDN |
  | `/static/` (Admin, DRF) | `runserver` (`DEBUG=True`) 또는 nginx (`DEBUG=False`) |

  `DEBUG=False`인 `prod`에서는 `runserver`가 정적 파일을 서빙하지 않습니다.
  배포 시 `collectstatic`으로 `server/staticfiles/`에 모은 뒤 nginx가 `/static/`을 해당 경로로 서빙해야 합니다.

  ```bash
  uv run python manage.py collectstatic --settings=config.settings.prod
  ```
- 시간대는 `Asia/Seoul`, `USE_TZ = True`로 설정되어 있습니다.
  DB에는 UTC 절대시각으로 저장되고, 출력(DRF / 템플릿 / admin)은 KST로 변환됩니다.
