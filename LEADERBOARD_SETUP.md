# Leaderboards: setup checklist (version 1.1)

The game's leaderboard code is done:

- `Scripts/Core/leaderboard.gd` (autoload `Leaderboard`): talks to Talo, sends personal bests,
  queues them while offline, reads boards, handles the nickname.
- `Scripts/UI/leaderboard_screen.gd`: the LEADERBOARD screen (top 100 + your rank, `<` `>` to
  change level, change your name).
- `Scripts/Config/leaderboard_config.gd`: the switches and numbers (anti-cheat floor, top count).
- Hooks: a gold **LEADERBOARD** button under START on the level screen (shows `#12` once you have a
  rank), and a "NEW WORLD RANK: #12!" line on the results screen.

Until the Talo plugin is installed, none of this shows in the game: no button, nothing sent.

## How it behaves

- **One board per level**, fastest time first, named `1_v1` … `10_v1`. If you rebuild a level,
  bump its number in `leaderboard_config.gd` `BOARD_VERSIONS` (e.g. `{7: 2}`) and create board
  `7_v2` in Talo, so old-layout times never mix with new ones.
- **Only personal bests are sent.** Anything not sent yet (finished offline, or set in 1.0 before
  boards existed) goes up the next time the game is online, including the moment the leaderboard
  screen is opened.
- **Player identity** is a random ID made on first launch, kept in `user://leaderboard.cfg`.
  Settings > Reset All Data does *not* erase it, so a reset doesn't put a second copy of the player
  on the boards (their old times stay there; a faster run still replaces them).
- **Nickname**: new players get `Shape1234`. The first time they open a board they're asked to pick
  one ("Later" keeps the default). 3 to 16 letters, numbers, spaces, `_` or `-`. Talo rejects
  names with profanity, and the game tells the player to try another.
- **Anti-cheat**: times faster than `gold time x 0.6` are refused before sending, and debug builds
  (the editor, debug exports) never send. To tighten a level, put its simulated fastest time minus
  a margin in `MIN_TIMES` in `leaderboard_config.gd`. Cheats that get through can be hidden or
  deleted in the Talo dashboard.

## 1. Talo account and game (you)

1. Sign up at trytalo.com and create a game ("Geometrical Haven"). The free Indie plan covers up
   to about 10K players; check the current limits and inactive-player rules on the pricing page.
2. **Game settings**: set the **display name prop key** to `nickname`. (Without it the boards still
   work: the game falls back to the name sent with each time, but renames only show on new bests.)
3. **Access keys**: create one key with these scopes:
   `read:players`, `write:players`, `read:leaderboards`, `write:leaderboards`,
   `write:continuityRequests`.
4. **Leaderboards**: create these 10, each with **sort mode: ascending (lowest first)**,
   **unique entries: on**, refresh interval: never.

   Internal names: `1_v1` `2_v1` `3_v1` `4_v1` `5_v1` `6_v1` `7_v1` `8_v1` `9_v1` `10_v1`
   (unique by prop: off).

   (Running the game from the editor prints this list in the Output panel once Talo is installed.)

## 2. Install the plugin (you)

1. In Godot: **AssetLib** tab, search "Talo Game Services", download and install. Only install it
   from the Asset Library or Talo's itch.io page (Talo's own docs warn against other sources).
2. **Project > Project Settings > Plugins**: enable Talo. This adds its `Talo` autoload.
3. Run the game once: the plugin creates `addons/talo/settings.cfg`. Paste the key into
   `access_key`. That file is in `.gitignore`, so the key doesn't end up on GitHub.

## 3. Test (you)

1. Debug runs don't send times. To test uploading, set `SUBMIT_FROM_DEBUG_BUILDS := true` in
   `leaderboard_config.gd`, play a level, check the entry in the Talo dashboard, then **set it back
   to false and delete your test entries** before shipping.
2. Reading boards works from the editor without changing anything: open LEADERBOARD on the level
   screen.
3. Offline: turn on airplane mode, finish a level with a new best (results say "World time uploads
   when you're online"), turn it off, open LEADERBOARD: your time should appear.
4. Try a rude nickname: it should be refused with "That name isn't allowed."

## 3b. Weekly challenge (you)

Code: `Scripts/Core/weekly.gd` (autoload `Weekly`), the WEEKLY tab in `leaderboard_screen.gd`,
settings at the bottom of `leaderboard_config.gd`.

How it works:
- **One level a week**, the same for everyone, picked from `WEEKLY_LEVELS` in a fixed shuffle: each
  level once every 10 weeks, never twice in a row. Weeks start **Monday 00:00 UTC** (Sunday 6 pm
  in Alberta). Players who haven't unlocked that week's level see "Unlock level N to join".
- Any run on that level during the week counts (your fastest that week). It also still counts for
  the level's normal board.
- **Rewards** for the final rank: #1 1000 coins, #2 600, #3 300, #4-50 50, #51-100 10
  (`WEEKLY_REWARDS`). Opening LEADERBOARD after the week ends shows "Last week's results" with a
  CLAIM button, then this week's board. Results wait up to 4 weeks. Each week pays once per device
  (remembered in `user://weekly.cfg`, which Reset All Data doesn't erase).
- The LEADERBOARD button says **NEW** until the new week's board has been opened.

In the Talo dashboard, create **one** more leaderboard:

| Setting | Value |
|---|---|
| Internal name | `weekly` |
| Sort mode | ascending (lowest first) |
| Unique entries | **on** |
| Unique by props | **on** (each time is tagged with its week, so this keeps one entry per player per week) |
| Refresh interval | never (the game handles weeks itself) |

Test without waiting a week (debug builds only, in `leaderboard_config.gd`):
- `DEBUG_FAKE_ENTRIES := 100` shows a made-up weekly board, and pretends you played last week, so
  opening LEADERBOARD shows the results panel (you at `DEBUG_FAKE_MY_RANK`, e.g. 37 = 50 coins).
- `DEBUG_WEEK_OFFSET := 1` pretends a week has passed, for testing with real times: play this week's
  level (with `SUBMIT_FROM_DEBUG_BUILDS := true`), set the offset to 1, run again, open LEADERBOARD.
- Test claims are saved in `user://weekly_debug.cfg`, so they never block real claims. Set both
  back to 0 when done.

## 3c. Weekly notifications (you)

Code: `Scripts/Core/reminders.gd` (autoload `Reminders`). One local notification is kept
scheduled for **6 pm the player's time on the first evening of each new week** (`NOTIFY_LOCAL_HOUR`):
"New weekly challenge! ... Last week's results are in. See your rank and claim your coins!" Tapping
it opens the weekly board. The phone asks for permission the first time the WEEKLY tab is opened.
Settings has a "Weekly reminders: ON/OFF" button. Local notifications send no data anywhere.

Until the plugin is installed this does nothing (and the Settings button stays hidden).

1. **AssetLib**: install **"Android Notification Scheduler Plugin"** and **"iOS Notification
   Scheduler Plugin"** (by cengiz-pz, godot-sdk-integrations, v5.x; both share one interface, so
   ignore the file-conflict warning when installing the second). Install to the project root.
2. **Project Settings > Plugins**: enable it. For iOS, also enable it in the iOS export preset.
3. Android's status-bar icon is the game's own (a triangle with a ring), already in the project.
4. Test on a phone with a **debug** build (Godot's one-click deploy), not the editor. Set
   `DEBUG_NOTIFY_SECONDS := 60` in `leaderboard_config.gd`, open the WEEKLY tab, allow
   notifications, put the game in the background and wait a minute. Release builds ignore it.
   The status-bar icon is `assets/NotificationSchedulerPlugin/android/drawable/ic_notification_haven.xml`
   (if you reinstall the plugin, keep this file).
5. Check the Android export's permissions: the plugin needs "Post notifications". The game doesn't
   need exact alarms, so don't turn on "Schedule exact alarm" (Google Play restricts it).

## 4. Before release

Done already (Nov 22, 2026), live once you push `docs/`:
- **Terms of service** (`docs/terms.html#leaderboards`): new section 3 "Leaderboards and the weekly
  challenge" (nickname rules, fair play, weekly rewards, reporting a name); progress line fixed.
- **Privacy policy** (`docs/privacy.html`): new "Online leaderboards" section (Talo, random player
  ID, nickname, best times, shown publicly, not used for ads, how to delete).
- **Delete-data page** (`docs/delete-data.html#leaderboards`): new step 2, "Delete your leaderboard
  data": players email their nickname.
- **Website FAQ** (`contact.html`, from `build.py`): leaderboard data, offline play, and how to
  report an offensive nickname.
- **Privacy policy** also covers weekly-challenge times, notifications, Talo receiving the IP
  address, and reporting names.

When a deletion email arrives: find the nickname on a board in the Talo dashboard, delete that
player, and reply to confirm (within 30 days, as the page promises).

### Google Play Console → App content → Data safety (you, when you submit 1.1)

Don't change it before the 1.1 build is submitted: 1.0 doesn't send any of this. Keep every
existing AdMob answer and add:

| Section | Data type | Collected | Shared | Ephemeral | Required / optional | Purpose |
|---|---|---|---|---|---|---|
| Personal info | **User IDs** (random player ID) | Yes | No | No | Required | App functionality |
| App activity | **Other user-generated content** (nickname) | Yes | No | No | Required | App functionality |
| App activity | **Other actions** (best time per level) | Yes | No | No | Required | App functionality |

- "Shared" is No: Talo is a service provider processing data for you, which Google doesn't count
  as sharing.
- Encrypted in transit: **Yes** (HTTPS).
- Users can request deletion: **Yes**. Deletion URL:
  `https://neonafterglow.github.io/delete-data.html#leaderboards`
- "Does your app let users create an account?" stays **No**: the player ID is anonymous, with no
  sign-up, email or password.

### Google Play Console → App content → Content rating (you, when you submit 1.1)

Redo the questionnaire (IARC). Keep the 1.0 answers, but: players choose nicknames other players
can see, so answer **Yes** to the question about users sharing content or interacting
(user-generated content). There's no chat, messaging, location sharing or purchases of
real-world goods. The weekly coin prizes are skill-based in-game rewards, not gambling.
The rating may go up a step; that's expected.

### Reports and deletion requests (you, after release)

- **Reported nickname** (email): find it on the board in the Talo dashboard. Rename it (edit the
  player's `nickname` prop) or delete the player if it breaks the rules (Terms section 3).
- **Deletion request**: delete the player in the Talo dashboard, reply to confirm within 30 days.

### App Store Connect → App Privacy (you, when you submit 1.1 on iOS)

Already written into `store_listing/ios/APP_STORE_LISTING.md` (App Privacy section): add User ID,
Gameplay Content and Other User Content, all for App Functionality, linked to the user, not used
for tracking.
