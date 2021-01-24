# ModMail
## Discord bot used to send anonymous messages to the moderators

### Setup  
#### Dependencys
| Name| installation instructions | 
| ------------- | -------------------------------------------------------- |  
| A discord bot |  https://discordpy.readthedocs.io/en/latest/discord.html |
| Docker |  https://docs.docker.com/engine/install/ |
| docker-compose =< 1.27 |  https://docs.docker.com/compose/install/ | 
 
### Installation instructions
#### Make sure you put your own secrets into the config files before you build the container
```
$ git clone https://github.com/NetworkChuckDiscord/Modmail.git && cd Modmail
$ nano .mongoenv.sample # set the mongodb password here
$ cp .mongoenv.sample .mongoenv
$ nano .discordenv.sample # set your discord-token and use the same password as set earlier
$ cp .discordenv.sample .mongoenv
$ docker build . -t modmail
$ docker compose up -d
```

## Usage

Once the bot is added to your server, you can interact by sending it a DM. When you do that the bot will create a channel in the catagory named tickets and anonymously forward the messages from that user into that channel. Any responses written in that channel will then be DMed to the user.

| permision | Command | Description |
|-----------|---------|-------------|
| Admin | &search [ticket-number] | Type is the search you want to use can be 1) -ltdate -etdate -author and term is the search term |
| Admin | &user_search [uid] | prints all tickets submitted by that user | 
| Admin | &mod_search [uid] | prints all tickets that the moderator has been involved | 
| Admin | &close | Archives the complaint putting a full transcript in admin log |
| Admin | &force_close | Archives the complaint putting a full log in admin log without DMing the owner. Only use when the owner has left the server | 

## Configuration

### none of these work

There is currently no config file that is still in the works:

| Setting | default Value | Description |
|---------|---------------|-------------|
| prefex | & | sets the default command prefex
| ticket_catagory | Null | catagory where the complaint channels are placed | 
| complaint_log | Null |log where archived messages go |
