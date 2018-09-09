# Kaldığım Yer: Sayfa 182 Testing Interactions


### Finished code for part - 1 : 
https://github.com/testdrivenio/testdriven-app-2.2/releases/tag/part1

### pushing tags to remote

```bash
git push origin <tag_name>  # pushes specific tag

git push --tags  # pushes all tags (not recommended)
```

### creating tags for specific commit

```bash
git log --pretty=oneline 

544be295370d4f27eab6c4d3238256f91ffea167 (HEAD -> master, tag: postgres_completed, origin/master) postgres ekleme tamamlandı
fbce5c4786fe3662c3a2c0a2650589508a1ea637 (tag: postgres_final) postgres eklendi
99141aae0605cc4943940503f37b6f2841be0f98 user dockerized
bf20168fdaacf97e8480ecac01e8a960226cd76a initial commit

# örneğin 9911 ile başlayan için tag eklemek istersek:

git tag -a "user_dockerized" 9914
```


### create react app
```bash

create-react-app .

```

### start react app develeopment
```bash
npm start

```

### create react app build
```bash
npm run build
# bu komutu react app 'in olduğu klasörden vermek gerek

```


## Links:
* https://reacttraining.com/react-router/web/guides/quick-start


## Testing Workflow:

```bash
# update the containers and ensure the app working on client:
docker-compose -f docker-compose-dev.yml up -d

# test python code
docker-compose -f docker-compose-dev.yml run users python manage.py test

# test react client code
docker-compose -f docker-compose-dev.yml run client npm test
```