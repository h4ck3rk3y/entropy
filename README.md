# entropy

![](https://cdn.pixabay.com/photo/2016/09/16/19/12/atom-1674878_960_720.png)

the natural state of entropy is to increase. we must fight against it. 💪

entropy is a command line friend that helps you reduce entropy
in your life

## Installation

### 1: [PIP](https://pypi.python.org/pypi/entropy)

```bash
$ pip install entropy
```

### 2: From source

```bash
$ git clone https://github.com/h4ck3rk3y/entropy
$ cd entropy
$ python setup.py install
```

## Usage

### Tell entropy how today went

``` bash
$ entropy status add
```

### Ask entropy at how today, yesterday, week, month, year and lfie have been going

```bash
$ entropy status view today
$ entropy status view yesterday
$ entropy status view week
$ entropy status view month
$ entropy status view year
$ entropy status view life
$ entropy status view YYYY-mm-dd
```

### Journal with entropy every morning

```bash
$ entropy journal add
```

### Ask entropy to retrieve older journals for you

```bash
$ entropy journal view today
$ entropy journal view yesterday
$ entropy journal view YYYY-mm-dd
```

### If you need help, don't be shy

```bash
$ entropy --help
```

## Contributing

Use the [Github](https://github.com/h4ck3rk3y/entropy) to file bugs or push new features.

## License

Open sourced under the **MIT License**