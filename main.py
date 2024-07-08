import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # Ensure the response is decoded as UTF-8
    return response.text

def get_specific_field(content, css_selector):
    """
    Extract the content of a specific field using a CSS selector.
    """
    soup = BeautifulSoup(content, 'html.parser')
    elements = soup.select(css_selector)
    return "\n".join([element.get_text(strip=True) for element in elements])

def send_discord_notification(webhook_url, message):
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    response.raise_for_status()

def main():
    url = "https://trouverunlogement.lescrous.fr/tools/34/search?bounds=-0.6386987_44.9161806_-0.5336838_44.8107826"  # Replace with the URL you want to monitor
    css_selector = ".SearchResults-desktop"  # Replace with the CSS selector of the specific field you want to monitor
    discord_webhook_url = "https://discordapp.com/api/webhooks/1259477262189727775/t92Saq-zeXVZ6jh_eOl-H7Rd2P0v_i9ETgtHQOO1Xr5KcfSWVfO3z7QySLJVbbt01tbw"


    # Read the old content if it exists
    old_content = "Aucun logement trouvé"


    # Get the content of the web page
    content = get_page_content(url)
    # Extract the specific field content
    field_content = get_specific_field(content, css_selector)

    # If there is a change, send a notification
    if old_content and field_content and (field_content != old_content):
        message = f"The content of the specific field in {url} has been updated."
        send_discord_notification(discord_webhook_url, message)
        old_content = field_content


if __name__ == "__main__":
    main()


