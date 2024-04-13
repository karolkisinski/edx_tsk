
# How to run

- clone this repository
```
https://github.com/karolkisinski/edx_tsk.git
```
- If you want to use docker then build image

```
docker build -t edx_tsk . 
```

- and access it with this command

```
docker run -it --rm edx_tsk sh

and after it move to src dir:
cd src

```

Available command (works also without docker):
```
inside src folder

python main.py -m mode -c currency_code -a amount

modes:
    - dev
    - prod

currency_code - 3 letters code for e.g. usd

amount: amount of currency

example usage:

python main.py --mode prod -c eur -a 125
```

To run tests inside src dir:

```
python -m unittest discover tests
```