# Quote It — User Guide

Welcome to **Quote It**, your personal collection of inspirational quotes, proverbs, and sayings paired with beautiful photography.
You can also create your own quotes with your own images, stored locally on your device.

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

### Study Details (iPad)
On large iPad layouts, supported study datasets can show a details panel.

- Choose section type (for example transliteration, word meanings, translation, commentary)
- Filter by language and provider/author when available
- In landscape, details appear as a right-side panel
- In portrait, details appear as a bottom split panel while quote/author stay readable in the top half
- Use the panel switch to hide/show details
- When details are hidden, use the top-right **Details** button (visible with toolbar) to bring the panel back

### Sharing a Quote
When you tap the share button, you'll see two options:

- **Share Text** — Shares quote text and author only
- **Share Image** — Creates a styled card and includes source credit links when using Unsplash/Pexels backgrounds

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

### Create Your Quote
- Use the **Create Your Quote** action in Explore to add your own quote text and image.
- You can import an image from Photos or capture one with Camera.
- New personal quotes are saved locally and automatically added to Favorites.

### Browse by Author
When you first open Explore, you'll see grouped/browsable entries based on the active dataset. Tap any entry to view matching quotes.

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

### Personal Quotes
- Use the **My Quotes** filter (person badge icon) to show only your own quotes.
- In Explore results, swipe a personal quote to **Edit** or **Delete** it.

---

## Favorites

The Favorites screen shows all quotes you've saved by tapping the heart icon. Favorites are stored locally on your device and persist between app launches.

- Tap any favorite to view it full-screen
- Tap the heart icon again on any quote to remove it from favorites
- Your favorites are never uploaded or shared — they stay on your device
- Use the **Create Your Quote** action to add a personal quote directly from Favorites
- Use the **My Quotes** filter (person badge icon) to show only your personal quotes
- Swipe personal quotes to **Edit** or **Delete**

---

## Settings

Settings is organized into grouped sections:
- **General**
  - **Daily Notifications**
  - **Appearance**
  - **Voice & Dictation**
- **Output**
  - **Export & Sharing**
  - **Storage**
- **Support**
  - **Help & About**

Each settings screen includes a short description so every option is self-explanatory.

### Daily Notifications
- **Enable Daily Quote** — Receive a notification once a day with an inspirational quote
- **Time** — Choose what time of day you'd like to receive the notification
- You'll need to grant notification permissions when prompted

### Appearance

#### Background & Layout
Control which photo services provide background images for your quotes.

- **Unsplash** — Toggle high-quality photos from Unsplash on or off
- **Pexels** — Toggle free stock photography from Pexels on or off
- **Download on Cellular** — Control whether images download on mobile data
- **Blur** — Softens image detail behind text
- **Dim Strength** — Darkens image for better quote readability
- **Gradient Tint** — Adds a mood color tint
- **Tint Strength** — Controls tint intensity
- **Zoom** — Controls background crop scale
- **Horizontal Position** / **Vertical Position** — Reposition image framing
- **Reset Background Controls** — Restores visual defaults

Disable both Unsplash and Pexels to view quotes without background images.

#### Quote Text Styling
- **Text Color** — Auto, light, dark, or gradient quote text modes
- **Decorative Quote Mark** — Shows/hides the large stylized opening quote mark behind the quote text

### Voice & Dictation
- **Use System Default Voice** — Follow iOS voice settings
- **Personal Voice** — Dedicated picker for Personal Voice when available and authorized
- **Standard Voice** — Choose a specific built-in system voice
- **Speech Rate** — Adjust read-aloud speed
- **Preview Voice** — Test current voice settings
- **Dictation** — In Create/Edit Quote, use Dictate Quote to transcribe speech into quote text

Personal Voice is available only after app-level permission is granted in Voice & Dictation and a Personal Voice is configured on the device.
Microphone permission handling for dictation uses the latest iOS APIs and remains compatible with older supported versions.

### Content & Navigation
- **Data Source** — Switch between all discovered bundled/imported sources
- **Reading Mode** — Random or Browse sequence
- **Auto Mode Switch** — When moving from `QuoteIt` to any other source, the app switches Reading Mode to `Browse`
- **Source Details** — Language, edition, and item count for the active source

### Source Import & Import Models
- Open **Settings > Content & Navigation > Open Import Wizard** to import local datasets.
- Import Wizard flow:
  - **File**: select source package/folder or raw file (`.txt`, `.md`, `.csv`, `.tsv`, `.json`, `.pdf`)
  - **Intent**: provide optional dataset hints
  - **Model**: choose runtime (`Rules Only`, `Bundled`, `Imported`, `Automatic`)
  - **Review**: inspect parsed records and refine selection
  - **Finalize**: publish source metadata and add to app
- Open **Manage Import Model** for model management (install, select active imported model, delete imported models).
- Model install methods:
  - **Install from URL**: direct `.mlmodel` or `.mlpackage` URL
  - **Install from Files (AirDrop)**: local `.mlmodel`, `.mlpackage`, or `.mlmodelc`
- If imported models exist, the app defaults runtime to **Automatic** (unless you explicitly set **Rules Only**).

### Export & Sharing
- **Layout** — Export framing/aspect preset
- **Quality** — Output quality and size
- **Style** — Export presentation style
- **Include Photo Attribution** — Adds photo credit in exported card when enabled
- **Accessibility Export Mode** — Improves readability in exported images

### Storage
Background images are stored locally for faster loading and offline use, with separate groups to avoid accidental deletion.

- **Cache Size** — Choose how many downloaded web images to keep cached (50–500)
- **Clear Web Image Cache** — Removes only downloaded Unsplash/Pexels cache entries
- **Clear Selected Photos Backgrounds** — Removes only backgrounds you added from Photos in background chooser
- **Custom Quote Photos** — Shows count of photos attached to custom quotes; these are removed when the quote is deleted

### Help & About
- **Help** — In-app quick reference for key app workflows
- **About** — App name and current version

### Export Behavior for Personal Quotes
- Exports for built-in catalog quotes include Quote It branding.
- Exports for your own created quotes do not include Quote It branding.

---

## Background Images

Quote It displays beautiful photography behind your quotes. Images are sourced from:

- **Unsplash** — High-quality free photos
- **Pexels** — Free stock photography

You can enable or disable each source independently in Settings > Appearance > Background & Layout.

### How It Works
- A new background image is fetched when you navigate to a new quote
- Images are cached on your device for quick access
- The app automatically adapts text colors based on image brightness — light text on dark images, dark text on light images
- Image photographer attribution is shown at the bottom of the quote screen
- Photographer name links to photographer profile; source name links to the photo page
- Tap the photo button to open **Choose Background**
- Use **Refresh from Web** to force a new online fetch attempt
- Use **Choose from Photos** to add your own image into the chooser
- Thumbnails show source badge: **Your Photo**, **Unsplash**, or **Pexels**
- Long-press a thumbnail to remove that specific background from Quote It storage

### Offline Use
Previously downloaded images are available offline from the cache. The app gracefully handles no-network situations by using cached images.

---

## iPad & Landscape

Quote It works on both iPhone and iPad, in portrait and landscape orientations. The action bar and tab bar stay compact and centered on wider screens so the background image remains visible.

For supported study datasets on iPad, Quote It presents supplemental context as:
- Side panel in landscape
- Top/bottom split in portrait

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
- **Dictate faster** — In Create/Edit Quote, use Dictate Quote to transcribe your voice
- **Save storage** — Adjust the image cache size in Settings if storage is a concern
- **Go image-free** — Disable both Unsplash and Pexels in Settings for a clean text-only experience

---

## Developer Reference

For dataset/source schema details (manifest, primary data, and supplemental data), see:
- `Documentation/4.6.0/DATASET_SCHEMA.md`
