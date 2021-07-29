# Youtube Channel Searcher

## 프로젝트 개요 

> 원하는 검색어로 원하는 권역에서 유튜브 채널 리스트를 검색할 수 있는 검색 API 입니다.

> 본 API 서버는 아래의 태크 스택을 기반으로 만들어졌습니다.
> 
> - 개발 언어: *python 3.8*
> - 검색 로그 기록: *mongoDB*
> - 어플리케이션 관리 : *Docker / Docker-Compose*
> - 서버 컴퓨팅: *AWS EC2*

> 본 서비스는 다음의 플로우로 사용됩니다. 
> 1. 사용자의 검색 쿼리를 받아 Youtube API 를 통해 로직에 따라 적합한 유튜버 검색
> 2. 적합한 인플루언서 리스트를 json 데이터로 리턴
> 3. 유저의 검색 기록을 비동기적으로 mongodb에 저장 

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

3. `/nginx/default.conf`에서 지정한대로, 5000번 포트를 리스닝하여 80번 포트(FastAPI가 띄어진)로 요청을 전달하게 됩니다.  
 


## 프로젝트 구조 
```
├── app                 Python(FastAPI) 소스파일
│   ├── model           검색 결과 모델 schema
│   ├── service         검색 로직
│   └── view            API 라우터 
├── mongodb             몽고DB 도커파일
└── nginx               nginx 설정파일 (config, Dockerfile)
```

## API 명세서
- [POST] influencer/search  
request body 로 application/json 타입의 입력을 받습니다.
```
{
  "keyword": "string",
  "region": "string",
  "max_subscriber": 0,
  "min_subscriber": 0
}
```
- keyword: 검색어입니다. 입력한 키워드 기반으로 채널을 운영하는 유튜브 채널을 검색합니다.
- region: 검색 권역입니다. 유튜브에서 사용하는 ISO 3166-1 alpha-2 코드를 값으로 받습니다.
- max_subscriber: 검색하려는 채널의 최대 구독자입니다.
- min_subscriber: 검색하려는 채널의 최소 구독자입니다.

- 반환 결과 
![image](https://user-images.githubusercontent.com/58629967/127467420-464d33ca-cca5-49aa-8051-c7b4d398a174.png)

