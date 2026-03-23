# NANCY VR Video Streaming Server with Analytics

A lightweight, dockerized video streaming server optimized for MP4 files with built-in streaming analytics.

## Quick Start

### Prerequisites

- Docker and Docker Compose
- A collection of MP4 video files

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Metamind-Innovations/nancy_vr_video_streamer.git
   ```
2. Copy your MP4 video files to the `videos` directory. Indicative VR videos regarding Ancient Greece could be
   found [here](https://uowmgr.sharepoint.com/:f:/r/sites/NANCYSNS/Shared%20Documents/WP6%20NANCY%20System%20Integration,%20Validation%20and%20Demo/Greek%20Outdoor%20Testbed/VR%20videos?csf=1&web=1&e=9l7Cnw).

3. Build and start the Docker container:
   ```bash
   docker-compose up
   ```
4. Access the video player at `http://localhost:8080`

## Local Network Deployment

To access the streaming server from other devices on your local network:

1. Find your computer's IP address:
    - **Windows:** Run `ipconfig` and look for IPv4 Address
    - **macOS:** Run `ifconfig | grep "inet " | grep -v 127.0.0.1`
    - **Linux:** Run `hostname -I`

2. Ensure port 8080 is allowed through your firewall:
    - **Windows:** Open Windows Defender Firewall > Advanced Settings > Inbound Rules > New Rule > Port > TCP > 8080
    - **macOS:** System Preferences > Security & Privacy > Firewall > Firewall Options > Add (+) > Allow incoming
      connections
    - **Linux:** Run `sudo ufw allow 8080/tcp`

3. Access from other devices using `http://YOUR_IP_ADDRESS:8080` (e.g., `http://192.168.1.5:8080`)

## Remote Access Deployment

For access from anywhere on the internet:

### Method 1: Port Forwarding (Home Network)

1. Access your router admin panel
2. Navigate to port forwarding settings
3. Forward external port 8080 to your computer's internal IP on port 8080
4. Find your public IP at [whatismyip.com](https://whatismyip.com)
5. Access via `http://YOUR_PUBLIC_IP:8080`

### Method 2: Temporary Public URL with Ngrok

1. Download and install [Ngrok](https://ngrok.com/download)
2. Run: `ngrok http 8080`
3. Use the generated URL (e.g., `https://a1b2c3d4.ngrok.io`)

### Method 3: Cloud Deployment (AWS, DigitalOcean, etc.)

1. Deploy your Docker container to a cloud provider
2. Ensure port 8080 is open in security group/firewall
3. Use the cloud provider's public IP or domain

## License

MIT License

## Acknowledgements

- Nginx for the robust web server
- Docker for containerization

🇪🇺 NANCY project has received funding from the European Union's Horizon Europe research and innovation programme under
**Grant Agreement No. 101096456**.

*Disclaimer: Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do
not necessarily reflect those of the European Union or European Commission. Neither the European Union nor the European
Commission can be held responsible for them.*