# onboarding-challenge
Initiation challenge presented in our onboarding guide for newcomers in our organization.

## Content

The onboarding challenge is divided into three notebooks. The first one presents how to detect an eye blink artefact in a given signal and how to record your own signals using [MuseLSL](https://github.com/alexandrebarachant/muse-lsl). The second one shows how to detect eye blinks in a real time signal and links it to a [runner game](https://github.com/shivamshekhar/Chrome-T-Rex-Rush). The third and final notebook shows how to filter the eye blink artefact out of the signal.

## Setup

The challenge is presented in a jupyter notebook. You must first install Python 3 [here](https://www.python.org/downloads/). Afterwards, just run the following command to install all required packages.

> pip install -r requirements.txt

You will then be able to start a new jupyter kernel with the following command.

> jupyter notebook

You can now open the `onboarding-challenge` notebook inside you browser and start experimenting.

### Submodule

In order to fetch the source code of the dino run, please type the following commands:

```
git submodule init
git submodule update
```

## Common issues

If you encounter issues regarding the connexion of the Muse headband, please refer to the [muse-lsl guide](https://github.com/alexandrebarachant/muse-lsl). You also have to make sure your bluetooth drivers are up to date (i.e. [bluez drivers](https://docs.ubuntu.com/core/en/stacks/bluetooth/bluez/docs/) if you are using linux). If you are working with Mac, a dongle is required to connect the Muse.
