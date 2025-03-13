# `Cloudflare Tunnel`

### **Step 1: Install Cloudflared on Ubuntu**
Run the following commands:

```bash
sudo apt update && sudo apt upgrade -y
```

Then, install Cloudflared:

```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
sudo chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/
```

Verify the installation:

```bash
cloudflared --version
```

---

### **Step 2: Start a Cloudflare Tunnel (Temporary)**
After installation, you can run a quick Cloudflare Tunnel like this:

```bash
cloudflared tunnel --url http://localhost:8000
```

This will generate a **public Cloudflare URL** that can be used to access your **localhost service**.
