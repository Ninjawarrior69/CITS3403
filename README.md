# CITS3403 Group Project

## Overview

BookWorm is a reading tracker web app where users can browse books, create an account,
and share their reading activity with others.

## Team

<div>
  <table text-align: center;>
    <tr>
      <th>Names</th>
      <th>Student Number</th>
      <th>Github Username</th>
    </tr>
    <tr>
      <td>Devarsh Patel</td>
      <td>22964473</td>
      <td>Ninjawarrior69</td>
    </tr>
    <tr>
      <td>Weiman Gao</td>
      <td>24084355</td>
      <td>WeimanGao</td>
    </tr>
    <tr>
      <td>Celeste Petrovski</td>
      <td>24224028</td>
      <td>CelestePetrovski</td>  
    </tr>
  </table>
</div>

## Prerequisites (Linux)

1. Install Python 3.10 or newer.
2. Verify Python and pip are available:

```bash
python3 --version
pip3 --version
```

## Run Application

1. Create a virtual environment:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip3 install -r requirements.txt
```

4. Start the Flask development server:

```bash
python3 run.py
```

5. Open http://127.0.0.1:5000 in your browser.

## Run Tests

### Running Unit Tests

To run the backend unit tests:

```bash
python -m unittest tests.unit_tests -v
```