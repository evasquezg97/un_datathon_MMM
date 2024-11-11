# Connected-Parches: Weaving a Sustainable Urban Tapestry in Medellín

**Connected-Parches** is an open-source platform designed to promote sustainable urban living in Medellín by connecting users with eco-friendly, culturally vibrant local businesses and green spaces. By leveraging advanced geospatial data, natural language processing, and text embeddings, *Connected-Parches* fosters an inclusive, sustainable, and resilient city. Developed as a participant in the UN Datathon, this project addresses key Sustainable Development Goals (SDGs) such as SDG 8, SDG 11, and SDG 12, aiming to create an immediate and scalable impact in Medellín’s tourism and local economy.

## Table of Contents
- [Connected-Parches: Weaving a Sustainable Urban Tapestry in Medellín](#connected-parches-weaving-a-sustainable-urban-tapestry-in-medellín)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Project Objectives](#project-objectives)
  - [Project Structure](#project-structure)
    - [Directory Details](#directory-details)
      - [`/ui`](#ui)
      - [`/ds`](#ds)
      - [`/data`](#data)
  - [Installation](#installation)
  - [Methodology](#methodology)
    - [Data Acquisition and Processing](#data-acquisition-and-processing)
    - [Technical Stack](#technical-stack)
  - [Platform Features](#platform-features)
  - [SDG Alignment and Impact](#sdg-alignment-and-impact)
  - [Future Vision](#future-vision)
  - [Contributing](#contributing)
  - [Authors](#authors)
  - [License](#license)

---

## Background

Medellín, globally recognized for its urban transformation, faces the challenge of balancing economic growth with social equity and environmental sustainability. Traditional tourism practices tend to spotlight high-traffic areas, overlooking sustainable, locally-owned businesses that could benefit from increased visibility and economic support. *Connected-Parches* aims to bridge this gap, positioning Medellín as a prototype for sustainable urban tourism that can be replicated in cities worldwide.

## Project Objectives

Our primary objectives for *Connected-Parches*, targeted for December 2024, are:

1. **Promote Sustainable Tourism**: Increase user engagement and web traffic to eco-friendly businesses by 30%.
2. **Support Local Enterprises**: Onboard at least 150 sustainable, locally-owned businesses.
3. **Enhance Urban Quality of Life**: Raise awareness and engagement with sustainable spaces by 20%.
4. **Generate Open Knowledge**: Release an open-source dataset cataloging Medellín’s sustainable businesses, green zones, and transport options.

## Project Structure

The repository is organized as follows:

```
├── ui/                    # Frontend code for user interaction and visualization
├── ds/                    # Data science and machine learning components
├── data/                  # Data processing, cleaning, and analysis
├── README.md              # Project overview and instructions
└── requirements.txt       # Python dependencies
```

### Directory Details

#### `/ui`
The `ui` directory contains the user interface code for *Connected-Parches*, designed for a seamless, visually engaging experience. Key components include:
- **Map and Recommendation Views**: Interactive maps displaying sustainable businesses and green zones.
- **User Preferences and Filters**: Options for users to set sustainability preferences, such as eco-certification and proximity to public transport.
- **API Integrations**: Connects to backend services for dynamic data retrieval and display.

#### `/ds`
The `ds` directory includes the core data science functionalities:
- **Recommendation Engine**: Provides personalized recommendations based on geospatial data and text embeddings from reviews and descriptions.
- **Visibility Balancing Algorithm**: Ensures a fair representation of popular and lesser-known local spots.
- **Natural Language Processing (NLP)**: Utilizes advanced embedding models (e.g., Large Language Models) to process reviews and descriptions, enhancing recommendation accuracy.
- **Geospatial Analysis**: Identifies green zones, public transport options, and sustainable businesses.

#### `/data`
The `data` directory is dedicated to data handling, including:
- **Data Collection and Ingestion**: Gathers data from sources mainly from scrapping, and so on.
- **Preprocessing**: Standardizes and cleans data for seamless integration across modules.
- **Exploratory Data Analysis (EDA)**: Analyzes datasets to identify trends, patterns...

## Installation

For each one of the directories (`ui`, `ds`, `data`), follow these steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/connected-parches.git
    cd connected-parches/FOLDER
    ```

2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

Keep following the instructions in each directory to set up the environment and run the project.

## Methodology

### Data Acquisition and Processing
1. **Ethical Data Collection**: Sources include public databases such as OpenStreetMap and Yelp.
2. **Geospatial Integration**: Open-source tools enrich data on locations, green zones, and transport.
3. **Text Embedding**: BERT and similar models analyze text for semantic relevance, enhancing recommendation quality.

### Technical Stack
- **Frontend**: Angular for an interactive user experience.
- **Backend**: Python (Django or Flask) for processing and API services.
- **Data Processing**: Pandas, NumPy for data handling; GeoPandas for geospatial data.
- **Machine Learning**: TensorFlow, PyTorch for NLP and recommendation models.
- **Database**: PostgreSQL.
- **Deployment**: AWS, utilizing free-tier services where possible.

## Platform Features

1. **Personalized Recommendations**: Tailored to user preferences, emphasizing sustainability.
2. **Interactive Geospatial Maps**: Visualize eco-friendly businesses and green zones.
3. **Visibility Balancing**: Algorithmically balances visibility between popular and lesser-known locations.
4. **Sustainability Indicators**: Integrates eco-certifications, local sourcing indicators.
5. **Community Engagement**: User reviews, ratings, and feedback encourage trust and transparency.
6. **Multilingual and Accessible Design**: Designed for inclusivity, supporting diverse users.

## SDG Alignment and Impact

*Connected-Parches* aligns with the following SDGs:
- **SDG 8 (Decent Work and Economic Growth)**: Promotes local sustainable businesses to boost the economy.
- **SDG 11 (Sustainable Cities and Communities)**: Supports sustainable tourism and equitable urban growth.
- **SDG 12 (Responsible Consumption and Production)**: Encourages users to choose responsible local enterprises.
- **SDG 17 (Partnerships for the Goals)**: Collaborates with local agencies and NGOs for collective impact.

## Future Vision

Connected-Parches envisions Medellín as a sustainable city model. Planned features include:
- **Enhanced Recommendation Algorithms**: Improved with real-time user behavior data.
- **Community Engagement Forums**: Enable user input and continuous platform refinement.
- **Scalability**: Expansion to other cities, creating a global framework for sustainable urban tourism.

## Contributing

We welcome contributions to make *Connected-Parches* more impactful. Please refer to the authors.

## Authors

- [Luis Miguel Montoya](https://github.com/LuisM31)
- [Juan José Rojas Velilla](https://github.com/Pansamaster)
- [Estevan Vasquez](https://github.com/evasquezg97)
- [Alejandro Sarasti](https://github.com/sarasti2)
- [Jose M Munoz](https://github.com/munozariasjm)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.