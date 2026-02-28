# Quote It — User Guide

Welcome to **Quote It**, your personal collection of inspirational quotes, proverbs, and sayings paired with beautiful photography.
You can also create your own quotes with your own images, stored locally on your device.

---

## Version 5.1.0 Highlights

- Multi-dataset reading with quick dataset switching from the Quote screen
- Explore search scope control: current dataset or all visible datasets
- New **For Me** tab for personalized recommendation flow
- Organized Choose Dataset with Quick Access + collapsible category/subcategory library
- Surprise Me shortcut (double-tap QuoteIt tabmakr) for random visible dataset + item + background
- Continuous Reader mode with Card/Reader transitions
- Swipe up/down in Card mode to enter Reader mode quickly
- Full-screen Quote Builder Wizard with style presets
- Full-screen Dataset Import Wizard with model-assisted review
- iPad supplemental details panel for supported study datasets
- Expanded Voice & Dictation controls with system and Personal Voice support
- Daily notification tap opens the exact item in-app when available

---

## Getting Started

When you first open Quote It, you'll see a random quote displayed over a background image. The app has five main sections accessible from the floating tab bar at the bottom of the screen:

1. **Quote** — The main screen with daily inspiration
2. **Explore** — Search and browse quotes/items across dataset scopes
3. **Favorites** — Your saved collection
4. **For Me** — Personalized feed surface (favorites/search-driven recommendations)
5. **Settings** — Preferences and help

---

## Quote Screen

The Quote screen is where you'll spend most of your time. It displays a full-screen quote with a background photograph.

### Navigation
- Tap the **right arrow** (chevron) on the action bar to see a new random quote
- Tap the **left arrow** to go back to the previous quote
- Tap anywhere on the screen to **show or hide** the toolbar and tab bar
- Double-tap quote text to toggle **Reader** / **Card** layout
- Swipe up/down in **Card** layout to quickly enter **Reader** layout
- Double-tap the **QuoteIt** tab button to run **Surprise Me** (random visible dataset + item + background)

### Reader Mode
- Reader mode shows quotes/items as a continuous stream separated by visual dividers.
- Scroll up/down to read previous and next entries continuously.
- In Reader mode, the centered item becomes the current item as you read.
- When you exit Reader mode, Card mode opens on the last centered item.
- Copy quick actions are available in Card mode (long-press), not in Reader mode.
- When Reader opens, a short tip reminds you that double-tap returns to Card mode.

### Action Bar
The floating action bar appears at the bottom of the screen with these actions:

| Icon | Action | Description |
|------|--------|-------------|
| Heart | **Favorite** | Save or unsave the quote to your Favorites |
| Speaker | **Listen** | Hear the quote read aloud using text-to-speech |
| Photo | **Choose Background** | Open background picker and refresh/favorite image options |
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
- **Share Image** — Creates a styled card and includes dataset photo credit links when using Unsplash/Pexels backgrounds

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

### Create Your Own
- Use the **Create Your Own** action in Explore to add your own text and image.
- You can import an image from Photos or capture one with Camera.
- New personal quotes are saved locally and automatically added to Favorites.

### Browse by Author
When you first open Explore, you'll see grouped/browsable entries based on the active dataset. Tap any entry to view matching quotes.

### Search
Use the search bar at the top to find quotes by:
- **Quote text** — Any words from the quote
- **Author name** — Full or partial name
- **Topic/tags** — Categories like "love", "wisdom", "success"

Use the scope control under the search field to choose:
- **All Datasets** — search across visible (not hidden) datasets
- **<Current Dataset>** — search only the active dataset

Search behavior:
- **Current dataset** search updates as you type (debounced).
- **All datasets** search runs when you tap keyboard **Search** (for better performance on large libraries).
- In **All Datasets** results, each row shows the dataset name badge.
- In current-dataset search, dataset badges are hidden (source is already obvious).

### Viewing Quotes
Tap any quote in a list to view it full-screen with a background image. From there you can:
- Use the action bar to favorite, listen, share, or save
- Navigate forward through the list using the arrow button
- Tap the back button (top-left) to return to the list

### Personal Quotes
- Use the **My Items** filter (person badge icon) to show only your own items.
- In Explore results, swipe a personal quote to **Edit** or **Delete** it.

---

## Favorites

The Favorites screen shows all quotes you've saved by tapping the heart icon. Favorites are stored locally on your device and persist between app launches.

- Tap any favorite to view it full-screen
- Tap the heart icon again on any quote to remove it from favorites
- Your favorites are never uploaded or shared — they stay on your device
- Use the **Create Your Own** action to add a personal item directly from Favorites
- Use the **My Items** filter (person badge icon) to show only your personal items
- Swipe personal quotes to **Edit** or **Delete**
- Use **Dataset Scope** to switch between:
  - **All Datasets** (favorites across every dataset)
  - **Current Dataset** (favorites only for the active dataset)

---

## For Me

`For Me` is the personalization surface for quote discovery.

- Uses your interactions (favorites, reading behavior, and search/open signals) to improve suggestions over time
- Uses the `sparkles` tab entry (`#F7C04A`) for clear discovery
- Shows a recommendation feed with reason chips (no separate search mode in this tab)
- Includes runtime controls:
  - **More Like This** — boosts similar items
  - **Less Like This** — suppresses similar results from the feed
  - **Reset** — clears For Me tuning signals
- Opens any selected item directly in the main Quote screen for normal reading flow

---

## Settings

Settings is organized into grouped sections:
- **General**
  - **Reading & Display**
  - **Daily Notifications**
  - **Voice & Dictation**
- **Output**
  - **Export & Sharing**
  - **Storage**
- **Library**
  - **Dataset Import**
- **Support**
  - **About & Help**

Each settings screen includes a short description so every option is self-explanatory.

### Daily Notifications
- **Enable Daily Notification** — Receive one notification each day with an inspirational item
- **Time** — Choose what time of day you'd like to receive the notification
- Tapping the notification opens that exact dataset item when it is still available
- You'll need to grant notification permissions when prompted

### Settings Search
- Use the search field at the top of Settings to find controls by keyword.
- Search results now support deep links to the exact setting row/control, not only the parent screen.
- When you open a result, the matched row receives a subtle temporary highlight so it is easy to spot.
- Going back from a result preserves your search term and result list so you can continue to the next match.

### Reading & Display

#### Background & Layout
Control which photo services provide background images for your items.

- **Unsplash** — Toggle high-quality photos from Unsplash on or off
- **Pexels** — Toggle free stock photography from Pexels on or off
- **Download on Cellular** — Control whether images download on mobile data
- **Blur** — Softens image detail behind text
- **Dim Strength** — Darkens image for better item readability
- **Gradient Tint** — Adds a mood color tint
- **Tint Strength** — Controls tint intensity
- **Zoom** — Controls background crop scale
- **Horizontal Position** / **Vertical Position** — Reposition image framing
- **Reset Background Controls** — Restores visual defaults

Disable both Unsplash and Pexels to view items without background images.

#### Text Styling
- **Quick Preset** / **Quick Layout** — Fast typography/layout bundles
- **Text Color** — Auto, light, dark, or gradient item text modes
- **Text Alignment** / **Vertical Placement** — Position item text and author
- **Text Size**, **Line Spacing**, **Letter Spacing**, **Text Opacity**, **Shadow Strength** — Fine typography controls
- **Decorative Quote Mark** — Shows/hides the large stylized opening mark behind the item text
- **Suggest for Current Background** — Applies readability-focused styling for the currently displayed image

### Voice & Dictation
- **Use System Voices** — Use installed iOS voices that match active dataset language
- **Personal Voice** — Dedicated picker for Personal Voice when available and authorized
- **System Voice** — Choose a specific built-in system voice
- **Speech Rate** — Adjust read-aloud speed
- **Preview Voice** — Test current voice settings
- **Dictation** — In Create/Edit, use Dictate to transcribe speech into item text

Personal Voice is available only after app-level permission is granted in Voice & Dictation and a Personal Voice is configured on the device.
Microphone permission handling for dictation uses the latest iOS APIs and remains compatible with older supported versions.

### Reading & Display (Navigation)
- **Reading Mode** — Random or Browse sequence
- **Auto Mode Switch** — When moving from `QuoteIt` to any other dataset, the app switches Reading Mode to `Browse`
- **Quick Dataset Chip** — On the main card screen (toolbar visible), use the dataset chip under Jump To to open full-screen **Choose Dataset**
- **Choose Dataset (Full Screen)** — Built for daily switching and list management (outside Settings):
  - `QuoteIt` is always first and required (cannot be hidden)
  - Starts with a **Quick Access** block that combines core, pinned, and recent datasets in one compact list (no subsection headers)
  - Main dataset library is organized into collapsible **Category** and **Subcategory** groups
  - Swipe left on dataset rows for **Pin/Unpin** and **Hide/Unhide**
  - Swipe left on eligible downloaded online datasets for **Delete** to remove local copy (built-in datasets cannot be deleted)
  - Swipe left on category/subcategory rows for bulk **Hide/Show** actions
  - **Show Hidden** top-left button reveals hidden datasets when needed
  - **Show Hidden** defaults to off each time the screen opens, so users see their focused visible list
  - Tapping a hidden dataset auto-unhides it and switches immediately
  - Dataset rows show visual state badges (for example **Online**, **Hidden**, **Pinned**) for quick scanning; built-in datasets do not show the **Online** badge
  - **Discover Online Datasets** is available directly inside Choose Dataset and only shows datasets not installed on this device
  - Deleted online datasets can be downloaded again anytime from Discover Online Datasets

### Dataset Import & Import Models
- Open **Choose Dataset > Discover Online Datasets** for quick install of missing public GitHub datasets.
- Open **Settings > Dataset Import > Import Wizard** to import local datasets.
- Import Wizard flow:
  - **File**: select dataset package/folder or raw file (`.txt`, `.md`, `.csv`, `.tsv`, `.json`, `.pdf`)
  - **Intent**: provide optional dataset hints
  - **Model**: choose runtime (`Rules Only`, `Bundled`, `Imported`, `Automatic`)
  - **Review**: inspect parsed records and refine selection
  - **Finalize**: publish dataset metadata and add to app
- Open **Settings > Dataset Import > Import AI Models** for model management (install, select active imported model, delete imported models).
- Model install methods:
  - **Install from URL**: direct `.mlmodel` or `.mlpackage` URL
  - **Install from Files (AirDrop)**: local `.mlmodel`, `.mlpackage`, or `.mlmodelc`
- If imported models exist, the app defaults runtime to **Automatic** (unless you explicitly set **Rules Only**).
- Source package sharing (`.quoteit`) uses an encrypted anti-tamper envelope for exports.
- Legacy plaintext `.quoteit` packages are still accepted on import for compatibility.
- Discover Datasets supports install/update from `.quoteit` package URLs defined in catalog metadata.

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
- **Custom Item Photos** — Shows count of photos attached to custom items; these are removed when the item is deleted
- **Dataset Performance Cache** — Large datasets use on-device cache databases for faster load/search; you can clear and rebuild this cache in Storage

### About & Help
- **Help** — In-app quick reference for key app workflows
- **About** — App name and current version

### Export Behavior for Personal Items
- Exports for built-in catalog items include Quote It branding.
- Exports for your own created items do not include Quote It branding.

---

## Background Images

Quote It displays beautiful photography behind your quotes. Images are sourced from:

- **Unsplash** — High-quality free photos
- **Pexels** — Free stock photography

You can enable or disable each source independently in Settings > Reading & Display > Background & Layout.

### How It Works
- A new background image is fetched when you navigate to a new quote
- Images are cached on your device for quick access
- The app automatically adapts text colors based on image brightness — light text on dark images, dark text on light images
- Image photographer attribution is shown at the bottom of the quote screen
- Photographer name links to photographer profile; source name links to the photo page
- Tap the photo button to open **Choose Background**
- Use **Refresh from Web** to force a new online fetch attempt
- Use **Choose from Photos** to add your own image into the chooser
- Thumbnails show dataset badge: **Your Photo**, **Unsplash**, or **Pexels**
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

Watch support is enabled in the 5.1.0 release build.
It is available in 5.1.0 after release packaging hardening and signing updates.

---

## Home Screen Widget

Add a **Quote of the Day** widget to your home screen. The widget displays a new inspirational quote each day.

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

For dataset schema details (manifest, primary data, and supplemental data), see:
- `Documentation/4.6.0/DATASET_SCHEMA.md` (current schema reference used by 5.1.0)
