# ModMail
## Discord bot used to send anonymous messages to the moderators

### Setup  
#### Dependencies
| Name| installation instructions | 
| ------------- | -------------------------------------------------------- |  
| A Discord bot |  https://discordpy.readthedocs.io/en/latest/discord.html |
| Docker |  https://docs.docker.com/engine/install/ |
| Docker-compose =< 1.27 |  https://docs.docker.com/compose/install/ | 
 
### Installation instructions
#### Make sure you put your own secrets into the config files before you build the container
```
$ git clone https://github.com/NetworkChuckDiscord/Modmail.git && cd Modmail
$ nano .mongoenv.sample # set the mongodb password here
$ cp .mongoenv.sample .mongoenv
$ nano defaults.py # set default settings in here see chart below for descriptions
$ nano .discordenv.sample # set your discord-token and use the same password as set earlier
$ cp .discordenv.sample .mongoenv
$ docker build . -t modmail
$ docker compose up -d
```

## Usage

Once the bot is added to your server, you can interact by sending it a DM. When you do that the bot will create a channel in the catagory named tickets and anonymously forward the messages from that user into that channel. Any responses written in that channel will then be DMed to the user.

| permision | Command | Description |
|-----------|---------|-------------|
| Admin | &search [ticket-name] | Prints a transcript of the provided ticket |
| Admin | &user_search [uid] | Prints all tickets submitted by that user | 
| Admin | &mod_search [uid] | Prints all tickets that the specified moderator has sent a message in| 
| Admin | &close | Archives the complaint putting a full transcript in admin log and DMing it to the ticket owner |
| Admin | &force_close | Archives the complaint putting a full log in admin log without DMing the owner. Only use when the ticket owner has left the server | 
| admin | &lookup | search for setting name, uses difflib to find the closest matches | 
| admin | &reload | reload the bot listners, command, prefix |
| admin | &set [key] [value] | Set a setting and value (setting must exist)
| all | &help | shows a help message |

## Configuration

| Setting | Description |
|---------|-------------|
| prefex | sets the default command prefex
| catagory_id | category where the complaint channels are placed | 
| log_channel_id | channel where closed tickets go | 
| command_channel_id | channel where command respnses go | 
