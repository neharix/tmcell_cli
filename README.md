# TMCELL CLI Client (Inspired by [Lunatik-cyber's project](https://github.com/Lunatik-cyber/TMCELL_profile))

TMCell CLI Cabinet is a console Python interface for managing the personal account of a TMCell subscriber. Allows you to quickly manage packages, tariffs, services, send SMS, view your balance, payment and transfer history, and manage accounts directly from the terminal.

(Demo Version)

## Getting Started

### Prerequisites

Make sure you have Python 3.13 or newer version and poetry installed. Then install requirements:

```bash
poetry install
```

### Configuration

##### If you want to save your auth credentials:


1. Create the `.env` file:
   ```bash
   touch .env
   ```

2. Add "USER_LOGIN"(that is also your number) and "USER_PASSWORD"(can get it by sending a random sms to 0831) keys there
   ```plain
   USER_LOGIN=65000000
   USER_PASSWORD=YOURPASSWORD
   ```
3. Check the box next to Use environmental variables after you launch the application.


## Maybe Soon

- 🚀 **Faststream**: Integration with faststream for data retrieval in microservice environment

