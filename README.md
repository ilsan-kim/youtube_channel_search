# Youtube Channel Searcher

## 프로젝트 개요 

> 원하는 검색어로 원하는 권역에서 유튜브 채널 리스트를 검색할 수 있는 검색 API 입니다.

> 본 API 서버는 아래의 태크 스택을 기반으로 만들어졌습니다.
> 
> - 개발 언어: *python 3.8*
> - 검색 로그 기록: *mongoDB*
> - 어플리케이션 관리 : *Docker / Docker-Compose*
> - 서버 컴퓨팅: *AWS EC2*


## 배포 가이드
1. 로컬에서 작업 후 SCP 를 통해 EC2 인스턴스로 소스코드 압축하여 복사
```
cd 소스코드 경로
zip -r "youtuber_channel_searcher.zip"
scp -i .ssh/youtube_searcher.pem 소스코드경로/youtuber_channel_searcher.zip ubuntu@\[13.125.211.165\]:~
```

2. EC2 인스턴스에서 소스코드 압축 해제 후 도커 컴포즈 명령어 입력을 통해 배포
```
unzip youtuber_channel_searcher.zip
cd youtuber_channel_searcher
docker-compose up --build -d
```

## 프로젝트 구조 
```
├── app
│   ├── model
│   ├── service
│   ├── venv
│   └── view
├── mongodb
└── nginx

```

## API 명세서


## 주요 기능 설명    


## AWS 인스턴스 설정 내역
