#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <iomanip>

bool read_data(const std::string& filename, std::vector<double>& deviation_of_present_day, std::vector<double>& average_deviation_of_past_5days) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Could not open the file!" << std::endl;
        return false;
    }

    double deviation, average_deviation;
    std::string line;

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        ss >> deviation >> average_deviation;
        deviation_of_present_day.push_back(deviation);
        average_deviation_of_past_5days.push_back(average_deviation);
    }

    file.close();
    return true;
}

// Function to calculate the mean of a vector
double mean(const std::vector<double>& v) {
    double sum = 0;
    for (double value : v) {
        sum += value;
    }
    return sum / v.size();
}

// Function to calculate the covariance
double covariance(const std::vector<double>& x, const std::vector<double>& y, double x_bar, double y_bar) {
    double cov = 0;
    size_t n = x.size();
    for (size_t i = 0; i < n; ++i) {
        cov += (x[i] - x_bar) * (y[i] - y_bar);
    }
    return cov;
}

// Function to calculate the variance
double variance(const std::vector<double>& x, double x_bar) {
    double var = 0;
    size_t n = x.size();
    for (size_t i = 0; i < n; ++i) {
        var += (x[i] - x_bar) * (x[i] - x_bar);
    }
    return var;
}

int main() {
    std::vector<double> deviation_of_present_day; // Today's Deviation
    std::vector<double> average_deviation_of_past_5days; // Average Deviation of Past 5 Days

    // Read data from the text file
    if (!read_data("stock_data.txt", deviation_of_present_day, average_deviation_of_past_5days)) {
        return 1;
    }

    size_t n = deviation_of_present_day.size();
    if (n == 0) {
        std::cerr << "No data to process!" << std::endl;
        return 1;
    }

    // Calculate means
    double avg_deviation = mean(average_deviation_of_past_5days);
    double avg_present_deviation = mean(deviation_of_present_day);

    // Calculate beta1 and beta0
    double cov = covariance(average_deviation_of_past_5days, deviation_of_present_day, avg_deviation, avg_present_deviation);
    double var = variance(average_deviation_of_past_5days, avg_deviation);

    double beta1 = cov / var;
    double beta0 = avg_present_deviation - beta1 * avg_deviation;

    // Calculate R^2
    double RSE = 0;
    double TSS = 0;

    for (size_t i = 0; i < n; ++i) {
        double prediction = beta0 + beta1 * average_deviation_of_past_5days[i];
        RSE += (deviation_of_present_day[i] - prediction) * (deviation_of_present_day[i] - prediction);
        TSS += (deviation_of_present_day[i] - avg_present_deviation) * (deviation_of_present_day[i] - avg_present_deviation);
    }

    double R2 = 1 - (RSE / TSS);

    // Output the results
    std::cout << std::fixed << std::setprecision(4);
    std::cout << "beta1 = " << beta1 << std::endl;
    std::cout << "beta0 = " << beta0 << std::endl;
    std::cout << "R^2 = " << R2 << std::endl;

    return 0;
}
