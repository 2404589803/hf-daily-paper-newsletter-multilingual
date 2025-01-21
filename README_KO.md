# HuggingFace 일일 논문 뉴스레터

<div align="center">
  <a href="https://internlm.org/">
    <img src="https://internlm.org/assets/logo-a0611363.svg" alt="InternLM" height="80"/>
  </a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://huggingface.co/">
    <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="HuggingFace" height="80"/>
  </a>
</div>

<p align="center">
  <em>InternLM을 사용하여 HuggingFace 일일 논문 번역</em>
</p>

<div align="center">

[English](README.md) | [日本語](README_JA.md) | [한국어](README_KO.md) | [Español](README_ES.md) | [Français](README_FR.md)

</div>

---

이 프로젝트는 HuggingFace의 일일 논문 데이터를 자동으로 다운로드하고 처리하며, InternLM(서생·포어) 대규모 언어 모델을 사용하여 여러 언어로 번역합니다. 프로젝트는 매일 자동으로 실행되어 최신 논문의 수집과 번역을 보장합니다.

## 사용 모델

- **번역 모델**: [InternLM-3](https://internlm.org/)
  - 개발자: 상하이 인공지능 연구소
  - 버전: internlm3-latest
  - 특징:
    - 강력한 다국어 번역 능력
    - 학술 텍스트의 정확한 이해와 번역
    - API를 통한 실시간 번역

## 기능

- HuggingFace 일일 논문 데이터 자동 다운로드
- 지정 날짜의 과거 데이터 다운로드 지원
- 베이징 시간을 기본 시간대로 사용
- 완전한 로그 기록
- JSON 형식의 논문 메타데이터 저장
- InternLM-3을 사용한 영어 논문의 다국어 번역:
  - 일본어
  - 한국어
  - 스페인어
  - 프랑스어
- 자동화 워크플로우:
  - 매일 최신 논문 자동 다운로드
  - 자동 다국어 번역
  - 저장소 자동 업데이트

## 설치

1. 저장소 복제:
```bash
git clone https://github.com/yourusername/hf-daily-paper-newsletter-multilingual.git
cd hf-daily-paper-newsletter-multilingual
```

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법

### 수동 실행

#### 당일 논문 데이터 다운로드

```bash
python download_papers.py
```

#### 지정 날짜 논문 데이터 다운로드

```bash
python download_papers.py --date 2024-03-20
```

#### 논문 데이터 번역

InternLM API 키를 먼저 획득한 후 실행:

```bash
python translate_papers.py --date 2024-03-20 --api_key your_api_key_here
```

### 자동 실행

프로젝트에는 두 개의 GitHub Actions 워크플로우가 설정되어 있습니다:

1. `daily-paper-download.yml`: 매일 베이징 시간 9:00에 최신 논문 자동 다운로드
2. `daily-paper-translate.yml`: 다운로드 완료 후 자동 번역

자동 번역을 활성화하려면 저장소의 Secrets에 `INTERNLM_API_KEY`를 설정해야 합니다.

## 데이터 저장

- 다운로드한 원문(영어) 논문 데이터는 `Paper_metadata_download` 디렉토리에 저장
- 번역된 논문 데이터는 `Translated_papers` 디렉토리에 언어 코드별로 저장:
  - ja/: 일본어 번역
  - ko/: 한국어 번역
  - es/: 스페인어 번역
  - fr/: 프랑스어 번역
- 모든 파일은 JSON 형식으로 저장되며, 파일명은 `YYYY-MM-DD.json` 형식

## 반환 상태

- 성공: 종료 코드 0
- 오류: 종료 코드 1
- 데이터 없음: 종료 코드 0(단, 로그에 경고 표시)

## 감사의 말

- [InternLM](https://internlm.org/) - 강력한 번역 기능 제공
- [HuggingFace](https://huggingface.co/) - 일일 논문 데이터 제공 