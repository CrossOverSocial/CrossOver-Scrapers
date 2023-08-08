# CrossOver: Web Scraping Tools

## Overview

CrossOver is a web scraping toolset, initiated in 2021 with funding from the European Union’s programme on the financing of Pilot Projects and Preparatory Actions in the field of “Communications Networks, Content and Technology” under the grant agreement LC-01682253. The project was led by [EU DisinfoLab](https://disinfo.eu) in collaboration with [CheckFirst](https://checkfirst.network), [Apache](https://apache.be), and [Savoir-Devenir](https://savoirdevenir.net/). For more detailed information about the project, please visit [here](https://checkfirst.network/introduction-to-the-crossover-project/).

## Media Highlights

Here are some key media coverages that provide insights into the impact and relevance of the CrossOver project:

1. [Nieuws in de Klas](https://www.nieuwsindeklas.be/aan-de-slag-met-nieuws-in-de-klas/online-themadossiers/desinformatie/): This article discusses the role of CrossOver in combating disinformation in the digital age.

2. [Politico](https://www.politico.eu/newsletter/china-direct/britain-after-bojo-xi-biden-call-big-bridge-for-croatia/): This piece highlights the geopolitical implications of the CrossOver project.

3. [OpenFacto](https://openfacto.fr/2022/09/29/comment-la-fonction-dautocompletion-de-google-aide-a-la-diffusion-de-desinformation-sur-le-donbass/): This article delves into how Google's autocomplete function can inadvertently spread disinformation, and how tools like CrossOver can help mitigate this.

4. [Daar Daar](https://daardaar.be/rubriques/culture-et-medias/la-propagande-russe-simplante-solidement-en-belgique-grace-a-google/): This piece discusses the role of CrossOver in tracking and analyzing Russian propaganda in Belgium.

5. [Science Media Hub](https://sciencemediahub.eu/2023/02/15/science-and-tech-news-esmh-media-review-february-15-2022/): This article reviews the technological advancements of CrossOver in the field of data science and media.

## Installation

To install CrossOver, run the following command in your terminal: `pip install .`

For YouTube search emulation, you will need to install `youtube-dl`, a required dependency. Use the following command: `pip install -e git+https://github.com/ytdl-org/youtube-dl#egg=youtube_dl`

Please note that these commands may vary depending on your setup environment.

## Usage

### Google Autocomplete

Use `crossover -g -i queries.csv` to load an input file containing queries. For each entry, it returns the suggested autocomplete searches provided by the Google Autocomplete API. The responses are printed to stdout in a machine-readable format, along with a screenshot.

### YouTube Search Emulation

Use `crossover -y -i queries.csv` to load an input file containing queries. It simulates web browsing to the YouTube search page, parses all results, and collects their metadata. It then collects metadata from the recommended videos for each search result. All metadata are printed to stdout in a machine-readable format.

### Reddit Trends

Use `crossover -r -i queries.csv` to load an input file containing queries. It returns the trending posts of the corresponding subreddit. The returned metadata fields include ID, author, title, number of likes, number of comments, URL to the post, timestamp of content scraping, and timestamp shift (estimation of the post's age at the time of scraping).

### Twitter Trends

As of July 2023, due to changes applied by Twitter, this feature is no longer maintained.

## License

Please refer to the LICENSE file for licensing information.

## Copyright

© 2021 Check First OY