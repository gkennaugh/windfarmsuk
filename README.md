# <!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GNU License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/gkennaugh/windfarmsuk">
    <img src="images/windicss.svg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Wind Farms UK</h3>

  <p align="center">
    Dashboard to explore wind farms in the United Kingdom
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://gkennaugh9.eu.pythonanywhere.com/">View Live Demo</a>
    ·
    <a href="https://github.com/gkennaugh/windfarmsuk/issues">Report Bug</a>
    ·
    <a href="https://github.com/gkennaugh/windfarmsuk/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://gkennaugh9.eu.pythonanywhere.com/)

Dashboard with several pages to explore the data on United Kindgom wind farms. 

<p><b>Page 1</b> has maps to explore location of wind farms and average predicted wind speed for the area. </p>
<p><b>Page 2</b> has summary charts.</p>
<p><b>Page 3</b> shows electricity generation charts for individual wind farms.</p>
<p><b>Page 4</b> with maps and charts for general wind farm characteristics. Includes a table.</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Plotly][Plotly.com]][Plotly-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

The advantage of using plotly is everything from the front-end to the back-end is built using python. No need to learn javascript and seamlessly put online with https://pythonanywhere.com (free account to get you going). Pythonanywhere has most python packages installed on their own side so you just need to put your .py file and it should run straight away.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Install Python (better to use Anaconda https://www.anaconda.com/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/gkennaugh/windfarmsuk.git
   ```
2. Install required packages from requirements.txt
   ```sh
   pip install -r requirements.txt
   ```

3. Download the two largest files from here and store in the same directory as the other files:
   https://gkennaugh9.eu.pythonanywhere.com/static/shape25m2.csv
   <br>
   https://gkennaugh9.eu.pythonanywhere.com/static/roc2010-22(2).csv

4. Run python app_mobile.py in a new Anaconda Command Prompt (can take one minute to fully run first time)
   ```sh
   python app_mobile.py
   ```
   Open the app in your local browser at http://localhost:8061

N.B. You can use my api key to begin with but please get your own free key here https://www.mapbox.com/

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [-] Map info (location and predicted wind speed)
- [-] Exploratory charts for electricity generation
- [-] Match site names from two differently named databases
- [-] Obtain additional info from other online sources
    - [-] Monthly electricity generation for each individual wind farm for its lifetime
    - [-] Most recent (month) data for electricity generation
- [ ] Add offshore wind farms

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/oriondvd)) - info@oriondvd.co.uk

Project Link: [https://github.com/gkennaugh/windfarmsuk](https://github.com/gkennaugh/windfarmsuk)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/gkennaugh/windfarmsuk.svg?style=for-the-badge
[contributors-url]: https://github.com/gkennaugh/windfarmsuk/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/gkennaugh/windfarmsuk.svg?style=for-the-badge
[forks-url]: https://github.com/gkennaugh/windfarmsuk/network/members
[stars-shield]: https://img.shields.io/github/stars/gkennaugh/windfarmsuk.svg?style=for-the-badge
[stars-url]: https://github.com/gkennaugh/windfarmsuk/stargazers
[issues-shield]: https://img.shields.io/github/issues/gkennaugh/windfarmsuk.svg?style=for-the-badge
[issues-url]: https://github.com/gkennaugh/windfarmsuk/issues
[license-shield]: https://img.shields.io/badge/LICENSE-GNU%20V3-blue?style=for-the-badge&logo=GNU%20Privacy%20Guard
[license-url]: https://github.com/gkennaugh/windfarmsuk/blob/master/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[Plotly.com]: https://img.shields.io/badge/PLOTLY-Plotly.com-blue?style=for-the-badge&logo=Plotly
[Plotly-url]: https://plotly.com
