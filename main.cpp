/**
 * @file main.cpp
 * @brief Main file of the "Lamb" the discord bot.
 * 
 */
#include <nlohmann/json.hpp>
#include <fstream>
#include <Wool/Wool.hpp>

auto getSettings() {
    std::ifstream file("settings.json");
    nlohmann::json j;
    file >> j;
    file.close();
    return j;
}

int main() {
    auto settings = getSettings();
	Wool wool;
	wool.setPUBKEY(settings["PUBKEY"]);
	wool.setToken(settings["token"]);
	wool.run();
}