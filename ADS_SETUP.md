# Ads: setup checklist

The game's ad code is done: `Scripts/Core/ads.gd` (rules, rewards, stand-in test ads) and
`Scripts/Core/ads_admob.gd` (Google AdMob, used automatically once the plugin is installed).
All numbers and IDs are in `Scripts/Config/economy_config.gd` (the "ads" section).

Until the steps below are done, the game shows a stand-in **TEST AD** screen at every ad
moment, in the editor and on your phone, so everything can be tried now.

## How ads behave

- **Full-screen ads (interstitials)** appear only at a natural break: a crash's restart, or
  leaving the results screen. And only when all of these are true:
  - at least 10 crashes + finishes since the last ad,
  - at least 3 minutes since the last ad (the store's coin ads don't count),
  - at least 90 seconds into the session, and 5 minutes of total play ever,
  - not on the tutorial levels (1-3),
  - not within 2 minutes of watching a rewarded ad (the latest one restarts the 2 minutes;
    the store's coin ads don't count, only the results screen's "double it" ad),
  - at most 10 per session,
  - the player hasn't bought "Remove ads".
- **Rewarded ads** (always optional), up to 5 a day in total:
  - Store > "+" > "Watch an ad: +30 coins".
  - Results screen after a first-time medal: "Watch an ad: double it".
- While an ad shows, the game is frozen and the music pauses.

## 1. AdMob account (you)

1. Create an account at admob.google.com and add the app (Android).
2. Create two ad units: **Interstitial** and **Rewarded**.
3. ✅ Privacy & messaging: "Geometrical Haven - GDPR" (Consent / Do not consent / Manage
   options, 199 common ad partners; shown **everywhere**, so Quebec/Law 25 is covered) and
   "Geometrical Haven - US states" (opt-out) are published.
4. ✅ Done. Your IDs are in `economy_config.gd`:
   - App ID: `ca-app-pub-7361721628265043~6738388376`
   - Interstitial unit: `ca-app-pub-7361721628265043/6550686116`
   - Rewarded unit: `ca-app-pub-7361721628265043/7511579842`
   - Publisher ID `pub-7361721628265043` is in `docs/app-ads.txt`.

Debug builds automatically request Google's **test** ads (`ADMOB_TEST_ADS_IN_DEBUG`), so you
can't tap your own real ads by accident (AdMob can suspend the account for it). Only release
exports show real ads. New ad units can take an hour or so before they serve real ads.

## 2. Plugin (Godot editor) — Poing Studios AdMob 5.1

1. ✅ AssetLib → **AdMob** by Poing Studios → Install.
2. ✅ Project → Project Settings → **Plugins** → tick **AdMob** (Enabled). It downloads Google's
   Android libraries into `addons/admob/android/`. If that folder stays empty:
   Project → Tools → **AdMob Manager** → Android → Download & Install.
3. ✅ Project → Project Settings → General → **Admob → General → Android → App Id**:
   `ca-app-pub-7361721628265043~6738388376`. (The game crashes on launch with a wrong/missing ID.)
4. ✅ Project → Install Android Build Template; Export → Android → **Use Gradle Build** ticked.
5. ✅ Project Settings → Application → Config → **Name**: `Geometrical Haven` (the name under the
   app icon; it still says "Geometrical Shift").
6. ✅ Export → Android preset:
   - **Package → Unique Name**: `com.chasepelechytik.geometricalhaven` (permanent once it's on
     Play: the default `com.example...` is rejected by Play).
   - **Version → Name**: `1.0` (Code stays `1`; raise Code by 1 for every Play upload).
   - **Permissions**: tick **Internet** and **Access Network State**.
7. ✅ Deploy to your phone (debug) — consent form, coin ads and between-level ads all confirmed working: ads say "Test Ad". Quick tests:
   - Store → **+** → "Watch an ad: +30 coins" works straight away.
   - Between-levels ads need 5 min total play, 90 s into the session and 10 crashes/finishes.

To test the European consent form from outside Europe: run once, find the line in the log
that gives your device's hashed ID, and add it to `ADMOB_TEST_DEVICE_HASHES`.

## 3. ✅ Website: privacy policy + app-ads.txt (GitHub Pages, free) — live

Both files must be on a public website, and app-ads.txt must sit at the site's **root**.
A `neonafterglow.github.io` repository gives exactly that, and the game repo can stay private.

1. github.com → **New repository** → name it exactly `neonafterglow.github.io` → **Public** →
   tick "Add a README" → Create.
2. In the new repo: **Add file → Upload files** → drag in `index.html`, `privacy.html` and
   `app-ads.txt` from this `docs/` folder → **Commit changes**.
3. Settings → Pages: it should say the site is live (Source: Deploy from a branch, `main`, `/ (root)`).
   Give it a few minutes, then check:
   - https://neonafterglow.github.io/privacy.html
   - https://neonafterglow.github.io/app-ads.txt
4. `PRIVACY_POLICY_URL` in `economy_config.gd` already points at that privacy address
   (Settings in the game shows a "Privacy policy" button).
5. If you change these files later, upload them to that repo again.

Settings → **Privacy options** reopens Google's consent form; it shows only where the law
requires it (and always in debug builds, for testing).

## 4. Google Play Console

- App content → **Ads**: "Yes, my app contains ads".
- **Target audience**: 13+ (not designed for children; children's apps have much stricter
  ad rules).
- **Data safety**: declare that the app collects the device's advertising ID, approximate
  location (from IP) and app interactions, used by the Google Mobile Ads SDK for
  advertising/analytics, shared with Google. Data is encrypted in transit.
- **Privacy policy**: `https://neonafterglow.github.io/privacy.html`.
- Store listing → contact details → **Website**: `https://neonafterglow.github.io` (this is where
  AdMob looks for app-ads.txt).
- After the app is live on Play: AdMob → Apps → your app → **link it to the Play listing**.
  AdMob then checks app-ads.txt (can take up to 24 h; Apps → app-ads.txt shows the status).
- Real ads only show in release exports (debug builds use test ads). Play needs a release
  **AAB** signed with your own upload key (Export → Android → Keystore → Release).

## 5. Later: "Remove ads" purchase

`REMOVE_ADS_PRODUCT_ID` and the store's "Remove ads" button are ready. When a billing plugin is
added, switch on `PREMIUM_PURCHASES_ENABLED`, connect `Economy.purchase_requested` to it, and
call `Economy.complete_purchase(product_id)` when a purchase succeeds.
