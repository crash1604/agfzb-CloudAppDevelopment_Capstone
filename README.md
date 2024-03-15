# 🚗 Car Dealership Review Platform

Welcome to the Car Dealership Review Platform! This project represents the culmination of my journey through the IBM Full Stack Cloud Developer Professional Certificate on Coursera. Within this repository, you'll find a cloud-hosted web application built using Django and deployed on the IBM Cloud.

## ℹ️ About the Project

As the final Capstone Project, I embarked on creating a dynamic web platform that enables users to explore and review cars available at Best Car dealerships across the US. While the project's architectural foundation and design concept were provided, my focus was on implementing essential functionalities and back-end services as outlined by the course instructors.

## ✨ Key Features

- **Seamless Navigation**: Users can easily navigate through the site, accessing car dealership reviews and submitting their own feedback.
- **Cloud Integration**: Leveraging IBM Cloudant for dealership and review data storage, along with SQLite for user and car data management.
- **Sentiment Analysis**: Reviews are analyzed using IBM Watson to determine sentiment (negative, neutral, positive), enriching the user experience.

## 🛠️ Getting Started

To set up the project locally:

1. **Clone the repository**:

   ```
   git clone https://github.com/crash1604/agfzb-CloudAppDevelopment_Capstone
   ```

2. **Navigate to the project directory**:

   ```
   cd car-dealership-review-platform/server
   ```

3. **Install dependencies**:

   ```
   pip install -r requirements.txt
   ```

4. **Create a Django Secret Key**.

5. **Run the development server**:

   ```
   python manage.py createmigrations
   python manage.py migrate
   python manage.py runserver
   ```

6. **Access the application** through your web browser at `http://localhost:8000`.

## 🚀 Deployment

The application is deployed using Red Hat OpenShift/Kubernetes on the IBM Cloud.

## 📝 Feedback and Contributions

If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request. Your feedback is invaluable in enhancing the project for future learners.

## 🙏 Acknowledgments

I would like to express my gratitude to Coursera for providing this invaluable learning opportunity and to the course instructors for their guidance and support throughout the journey.

## 💡 For Coursera Learners

If you're currently undertaking the IBM Full Stack Capstone Project and find yourself stuck, don't hesitate to explore this repository for inspiration. Remember, learning is a collaborative journey, and together, we can empower one another to succeed!

Happy coding! 🌟
