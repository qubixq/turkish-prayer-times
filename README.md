# Turkish Prayer Times TUI

A terminal-based interface for Turkish prayer times, accessible via curl from anywhere.

## Usage

Get prayer times for any Turkish city using curl:

```bash
curl https://qubixq.github.io/turkish-prayer-times/ankara.txt
curl https://qubixq.github.io/turkish-prayer-times/istanbul.txt
curl https://qubixq.github.io/turkish-prayer-times/izmir.txt
```

## Features

- **81 Turkish cities** supported
- **Real-time prayer calculations** with current prayer status
- **Clean terminal display** with Unicode box drawing
- **Automatic daily updates** via GitHub Actions
- **Direct curl access** - no installation required

## Supported Cities

All 81 Turkish cities are supported using lowercase names:

`adana`, `adiyaman`, `afyonkarahisar`, `agri`, `amasya`, `ankara`, `antalya`, `artvin`, `aydin`, `balikesir`, `bilecik`, `bingol`, `bitlis`, `bolu`, `burdur`, `bursa`, `canakkale`, `cankiri`, `corum`, `denizli`, `diyarbakir`, `edirne`, `elazig`, `erzincan`, `erzurum`, `eskisehir`, `gaziantep`, `giresun`, `gumushane`, `hakkari`, `hatay`, `isparta`, `mersin`, `istanbul`, `izmir`, `kars`, `kastamonu`, `kayseri`, `kirklareli`, `kirsehir`, `kocaeli`, `konya`, `kutahya`, `malatya`, `manisa`, `kahramanmaras`, `mardin`, `mugla`, `mus`, `nevsehir`, `nigde`, `ordu`, `rize`, `sakarya`, `samsun`, `siirt`, `sinop`, `sivas`, `tekirdag`, `tokat`, `trabzon`, `tunceli`, `sanliurfa`, `usak`, `van`, `yozgat`, `zonguldak`, `aksaray`, `bayburt`, `karaman`, `kirikkale`, `batman`, `sirnak`, `bartin`, `ardahan`, `igdir`, `yalova`, `karabuk`, `kilis`, `osmaniye`, `duzce`

## Display Format

```
┌─────────────────────────────────────┐
│                ANKARA               │
├─────────────────────────────────────┤
│   İmsak       04:07           │
│   Güneş       05:52           │
│   Öğle        12:58           │
│   İkindi      16:47           │
│   Akşam       19:53           │
│   Yatsı       21:22           │
└─────────────────────────────────────┘
```

## Setup

1. Fork this repository
2. Enable GitHub Pages in repository settings
3. Set source to "GitHub Actions"
4. The workflow will run automatically daily at 6 AM Turkey time

## Local Development

```bash
pip install -r requirements.txt
python turkish_prayer_times_generator.py
```

## API Source

Prayer times are fetched from the Diyanet İşleri Başkanlığı API via ezanvakti.herokuapp.com.
