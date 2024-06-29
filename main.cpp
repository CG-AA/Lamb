/**
 * @file main.cpp
 * @brief Main file of the "Lamb" the discord bot.
 * 
 * using sleepy-discord library.
 */
#include "sleepy_discord/sleepy_discord.h"
#include <nlohmann/json.hpp>
#include <fstream>

auto getSettings() {
    std::ifstream file("settings.json");
    nlohmann::json j;
    file >> j;
    file.close();
    return j;
}

class MyClientClass : public SleepyDiscord::DiscordClient {
public:
	using SleepyDiscord::DiscordClient::DiscordClient;
	void onMessage(SleepyDiscord::Message message) override {
		if (message.startsWith("Hi Lamb!"))
			sendMessage(message.channelID, "Hello " + message.author.username + "!");
	}
};

int main() {
    auto settings = getSettings();
	MyClientClass client(settings["token"], SleepyDiscord::USER_CONTROLED_THREADS);
	client.setIntents(SleepyDiscord::Intent::SERVER_MESSAGES);
	client.run();
}