# Leaderboards and accounts: setup checklist (version 1.1)

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
- **Player identity is the player's account** (email + password, see section 1b). Guests can look
  at every board, but nothing is sent until they sign in; then the bests from their progress go up.
  The same account on any phone is the same player with the same name.
- **Nickname**: picked when the account is made (stored as the `nickname` player prop, so it
  follows the account). Change it on the account screen or the board's "Name:" button. 3 to 16
  letters, numbers, spaces, `_` or `-`, unique (capitals ignored). Talo rejects names with
  profanity, and the game tells the player to try another.
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
   `write:continuityRequests`, and for accounts (section 1b) `read:gameSaves`, `write:gameSaves`.
   (Edit the existing key to add the two save scopes; the key in `settings.cfg` stays the same.)
4. **Leaderboards**: create these 10, each with **sort mode: ascending (lowest first)**,
   **unique entries: on**, refresh interval: never.

   Internal names: `1_v1` `2_v1` `3_v1` `4_v1` `5_v1` `6_v1` `7_v1` `8_v1` `9_v1` `10_v1`
   (unique by prop: off).

   (Running the game from the editor prints this list in the Output panel once Talo is installed.)

## 1b. Accounts and cloud save (you)

Code: `Scripts/Core/account.gd` (autoload `Account`), `Scripts/Core/cloud_save.gd` (packing and
merging saves), `Scripts/UI/account_screen.gd` (the screen), settings in
`Scripts/Config/account_config.gd`. Opened from **Settings > Account** (title screen) and the
leaderboard's **SIGN IN TO POST YOUR TIMES** button.

How it works:
- **Talo Player Authentication** accounts, in the same Talo game, through the plugin you already
  have. No other plugin or service. Accounts are optional: the whole game plays without one.
- **Email + password.** The login name sent to Talo is a SHA-256 of the email (`gs_3f9a…`),
  because Talo includes every player's login name in leaderboard data that anyone with the app's
  key can read. Talo keeps the real email only for password reset emails. Never change
  `ID_SALT` in `account_config.gd` after release, or everyone gets locked out.
- **Cloud save:** one Talo save per account (named `progress`) holding the whole `save.cfg`
  (levels, times, coins, skins, themes, achievements, settings) and `weekly.cfg` (weekly times and
  claimed rewards), plus a revision number. Uploads 6 s after the last change, and when the app
  goes to the background. The phone checks for a newer copy at start-up, at sign-in and when the
  app comes back (at most once a minute). A newer copy reloads the game, so it waits while a level
  is being played.
- **Conflicts** (played offline on two phones, or a guest with progress signs in): the copies are
  merged so nothing is lost: faster best time, every unlock and owned item, larger counters, and
  coins = cloud + what this phone earned or spent since the last sync. Settings follow the cloud.
- **Sign out** uploads first (refuses while offline with unsaved progress), then wipes the phone
  back to a fresh guest. **Delete account** (needs the password) deletes the cloud save, then the
  Talo account and its leaderboard entries, then wipes the phone. **Reset All Data** while signed
  in also resets the cloud save (the account and its times stay).
- **Forgot password:** Talo emails a code; the player enters it with a new password. Login codes
  on every sign-in ("verification") are never turned on.
- **Weekly rewards** need an account, and claims are in the cloud save, so a week can't be claimed
  twice on two phones.
- Sessions last across restarts (Talo's refresh token, `user://talo_session.cfg`). If one runs
  out, the account screen says "Sign in again"; the phone keeps its progress meanwhile.

In the Talo dashboard:
1. Add the `read:gameSaves` and `write:gameSaves` scopes to the access key (section 1).
2. Open the game's settings and look at the **Player authentication** options: leave email
   verification off. If there's a setting for the password-reset email (sender name, game name),
   set it to "Geometrical Haven".
3. **Delete the test players from the nickname-only builds** (service `anonymous`) and their
   board entries, so the boards start with accounts only. The game also forgets those IDs on the
   phone (`user://leaderboard.cfg` with a `[player] id` is cleared on start-up).

Test (any build; accounts work from the editor):
1. Settings > Account > CREATE ACCOUNT with a real email of yours. Check the Talo dashboard:
   a player with a `talo` alias (`gs_…`), the `nickname` prop, and a save named `progress`.
2. Earn some coins, wait 10 s, then in the dashboard check the save's `rev` went up.
3. Sign out: the phone goes back to a fresh start. Sign in again: everything comes back.
4. Uninstall and reinstall (or delete the game's `user://` folder), sign in: everything comes back.
5. Two devices (phone + editor): play on one, then open the game on the other and sign in or
   bring it back to the foreground: the progress appears. Try airplane mode on one while playing
   on both, then reconnect: nothing is lost and coins add up.
6. Forgot password: the email with the code arrives (check spam), the new password works.
7. Delete account with a wrong password (refused, the save comes back), then the right one.
8. Leaderboard as a guest: boards show, the button says SIGN IN TO POST YOUR TIMES, the results
   screen says "Sign in (Settings > Account) to post world times".

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
  CLAIM button, then this week's board. Results wait up to 4 weeks. Needs an account. Each week
  pays once per account (remembered in `user://weekly.cfg`, which Reset All Data doesn't erase
  and which is part of the cloud save). Testing the results panel with `DEBUG_FAKE_ENTRIES` also
  needs you to be signed in.
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

Accounts (Nov 23, 2026), live once you push `docs/`:
- **Privacy policy**: new "Accounts and cloud save (optional)" section (email, password, cloud
  copy, how to delete); leaderboards now say they need an account.
- **Delete-data page** (`docs/delete-data.html#account`): new "If you have an account: delete it"
  (in the game, or by email from the account's address).
- **Terms**: progress line covers the cloud copy; a short "Accounts" rule.
- **FAQ** (`build.py`): "Do I need an account?" and the delete answer. Run `python3 build.py`.

When an account deletion email arrives: in the Talo dashboard find the player whose `talo` alias
is the email's code. To get the code, run in Godot's script editor (or ask Claude):
`print(preload("res://Scripts/Core/account.gd").login_id("their@email.com"))`. Delete its save,
then the player, and reply within 30 days.

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
| Personal info | **Email address** (account) | Yes | No | No | Optional | App functionality, Account management |
| Personal info | **User IDs** (account ID) | Yes | No | No | Optional | App functionality, Account management |
| App activity | **Other user-generated content** (nickname) | Yes | No | No | Optional | App functionality |
| App activity | **Other actions** (best times, cloud save of progress) | Yes | No | No | Optional | App functionality |

- "Shared" is No: Talo is a service provider processing data for you, which Google doesn't count
  as sharing.
- Encrypted in transit: **Yes** (HTTPS).
- Users can request deletion: **Yes**.
- "Does your app let users create an account?" **Yes**, with "Username and password" (email +
  password). Delete account URL: `https://neonafterglow.github.io/delete-data.html#account`
  (Google requires a web way to ask, besides the in-app button).
- "Optional": the whole game works without an account.

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

Already written into `store_listing/ios/APP_STORE_LISTING.md` (App Privacy section): add Email
Address, User ID, Gameplay Content and Other User Content, all for App Functionality, linked to
the user, not used for tracking. Give App Review a demo account (see that file).
