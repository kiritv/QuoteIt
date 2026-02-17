\# Quote It — User Guide

Welcome to **Quote It**, your personal collection of inspirational quotes, proverbs, and sayings paired with beautiful photography.

---

## Getting Started

When you first open Quote It, you'll see a random quote displayed over a background image. The app has four main sections accessible from the floating tab bar at the bottom of the screen:

1. **Quote** — The main screen with daily inspiration
2. **Explore** — Search and browse quotes by author
3. **Favorites** — Your saved collection
4. **Settings** — Preferences and help

---

## Quote Screen

The Quote screen is where you'll spend most of your time. It displays a full-screen quote with a background photograph.

### Navigation
- Tap the **right arrow** (chevron) on the action bar to see a new random quote
- Tap the **left arrow** to go back to the previous quote
- Tap anywhere on the screen to **show or hide** the toolbar and tab bar

### Action Bar
The floating action bar appears at the bottom of the screen with these actions:

| Icon | Action | Description |
|------|--------|-------------|
| Heart | **Favorite** | Save or unsave the quote to your Favorites |
| Speaker | **Listen** | Hear the quote read aloud using text-to-speech |
| Share | **Share** | Share the quote as text or as a styled image card |
| Download | **Save to Photos** | Save a styled quote card image to your Photos library |

The toolbar automatically hides after a few seconds to give you an unobstructed view of the quote. Tap the screen to bring it back.

### Sharing a Quote
When you tap the share button, you'll see two options:

- **Share Text** — Shares the quote text and author as plain text to any app (Messages, Notes, etc.)
- **Share Image** — Creates a beautifully styled card with the quote, author name, and background image, then opens the share sheet so you can send it anywhere

Shared images are cached to disk, so sharing the same quote again is instant.

### Saving to Photos
Tap the download icon to instantly render a styled quote card and save it to your device's Photos library. The card includes:
- The full quote text (centered)
- The author name
- The current background image (if available)
- Adaptive text colors based on image brightness

---

## Explore

The Explore screen lets you discover quotes by browsing and searching.

### Browse by Author
When you first open Explore, you'll see an alphabetically sorted list of all authors. Tap any author to see all their quotes.

### Search
Use the search bar at the top to find quotes by:
- **Quote text** — Any words from the quote
- **Author name** — Full or partial name
- **Topic/tags** — Categories like "love", "wisdom", "success"

Search results appear as you type with a short delay to keep the interface smooth. Search runs on a background thread so the UI stays responsive even with thousands of quotes.

### Viewing Quotes
Tap any quote in a list to view it full-screen with a background image. From there you can:
- Use the action bar to favorite, listen, share, or save
- Navigate forward through the list using the arrow button
- Tap the back button (top-left) to return to the list

---

## Favorites

The Favorites screen shows all quotes you've saved by tapping the heart icon. Favorites are stored locally on your device and persist between app launches.

- Tap any favorite to view it full-screen
- Tap the heart icon again on any quote to remove it from favorites
- Your favorites are never uploaded or shared — they stay on your device

---

## Settings

### Daily Notification
- **Enable Daily Quote** — Receive a notification once a day with an inspirational quote
- **Time** — Choose what time of day you'd like to receive the notification
- You'll need to grant notification permissions when prompted

### Background Images
Control which photo services provide background images for your quotes.

- **Unsplash** — Toggle high-quality photos from Unsplash on or off
- **Pexels** — Toggle free stock photography from Pexels on or off
- **Download on Cellular** — Control whether images download on mobile data

Disable both Unsplash and Pexels to view quotes without background images.

### Image Cache
Background images are downloaded and stored on your device for faster loading and offline use.

- **Cache Size** — Choose how many images to keep cached (50–500)
- **Clear Image Cache** — Remove all cached images to free up storage space. The app shows how many images were cleared.

### Help
A quick reference guide for the app's features is available in the Settings screen.

### About
Shows the app name and current version.

---

## Background Images

Quote It displays beautiful photography behind your quotes. Images are sourced from:

- **Unsplash** — High-quality free photos
- **Pexels** — Free stock photography

You can enable or disable each source independently in Settings > Background Images.

### How It Works
- A new background image is fetched when you navigate to a new quote
- Images are cached on your device for quick access
- The app automatically adapts text colors based on image brightness — light text on dark images, dark text on light images
- Image photographer attribution is shown at the bottom of the quote screen

### Offline Use
Previously downloaded images are available offline from the cache. The app gracefully handles no-network situations by using cached images.

---

## iPad & Landscape

Quote It works on both iPhone and iPad, in portrait and landscape orientations. The action bar and tab bar stay compact and centered on wider screens so the background image remains visible.

---

## Accessibility

Quote It supports VoiceOver and other assistive technologies:
- All action bar buttons have descriptive accessibility labels (e.g., "Add to favorites", "Read aloud", "Share quote", "Save to Photos")
- Tab bar items announce their label and selected state
- Quote content is combined for VoiceOver as "quote text, by author"
- The back button is labeled "Go back"

---

## watchOS Companion

Quote It includes a watchOS companion app that displays a **Quote of the Day** on your Apple Watch. The quote is selected deterministically based on the date, so you'll always see the same quote on the same day.

---

## Home Screen Widget

Add a **Quote of the Day** widget to your home screen. The widget displays a new inspirational quote each day, using the same deterministic selection as the watchOS companion.

Available in three sizes: **small**, **medium**, and **large**.

To add the widget: long-press your home screen, tap the **+** button, search for "Quote It", and choose your preferred size.

---

## Tips

- **Discover new quotes** — Keep tapping the forward arrow on the Quote screen to browse randomly
- **Build a collection** — Favorite quotes you love and revisit them anytime
- **Share beautifully** — Use "Share Image" to create styled cards perfect for social media
- **Listen while you work** — Use the speaker icon to hear quotes read aloud
- **Save storage** — Adjust the image cache size in Settings if storage is a concern
- **Go image-free** — Disable both Unsplash and Pexels in Settings for a clean text-only experience
