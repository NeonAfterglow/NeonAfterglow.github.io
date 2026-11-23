"""Builds the Neon Afterglow website (static HTML for GitHub Pages).

    python3 build.py            # writes the pages next to this file

Shared header/footer live here so every page stays consistent. The legal pages
(privacy, terms, delete-data) are restyled by wrap_legal() from their existing
content, keeping their URLs for Google Play and AdMob."""
import os, re, sys

SITE = "https://neonafterglow.github.io"
EMAIL = "neonafterglow06@gmail.com"
PKG = "com.chasepelechytik.geometricalhaven"
OUT = os.path.dirname(os.path.abspath(__file__))

from urllib.parse import quote


def email_btns(subject, body="", label="Email", cls="btn"):
    """Gmail button (works in any browser) + mail-app link + copy, since a bare
    mailto: does nothing on computers without a default mail app."""
    gmail = f"https://mail.google.com/mail/?view=cm&fs=1&to={EMAIL}&su={quote(subject)}" + (f"&body={quote(body)}" if body else "")
    mailto = f"mailto:{EMAIL}?subject={quote(subject)}" + (f"&body={quote(body)}" if body else "")
    return (f'<div class="btns" style="margin-top:14px">'
            f'<a class="{cls}" href="{gmail}" target="_blank" rel="noopener">{label} (Gmail)</a>'
            f'<a class="btn ghost" href="{mailto}">Mail app</a>'
            f'<button class="btn ghost copy-email" type="button">Copy address</button></div>')


COPY_JS = """<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
document.querySelectorAll('.copy-email').forEach(function (b) {
	b.addEventListener('click', function () {
		var email = '""" + EMAIL + """';
		var done = function () {
			var t = document.getElementById('toast');
			t.textContent = 'Copied: ' + email;
			t.classList.add('show');
			setTimeout(function () { t.classList.remove('show'); }, 2200);
		};
		if (navigator.clipboard && window.isSecureContext) {
			navigator.clipboard.writeText(email).then(done, function () { prompt('Copy this email address:', email); });
		} else {
			prompt('Copy this email address:', email);
		}
	});
});
</script>
"""


NAV = [("index.html", "Home"), ("games.html", "Games"), ("contact.html", "Contact")]


def head(title, desc, image="assets/gh-feature.jpg", path=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#07060f">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/{image}">
<meta property="og:url" content="{SITE}/{path}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
"""


def header(current):
    links = "\n".join(
        f'\t\t\t<a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>'
        for href, label in NAV)
    return f"""<header class="site-header">
	<div class="wrap">
		<a class="brand" href="index.html"><img src="assets/logo.png" alt="">Neon <span>Afterglow</span></a>
		<nav class="nav" aria-label="Main">
{links}
		</nav>
	</div>
</header>
"""


FOOTER = f"""<footer class="site-footer">
	<div class="wrap">
		<div>© 2026 Neon Afterglow · Indie games from Alberta, Canada</div>
		<nav aria-label="Footer">
			<a href="games.html">Games</a>
			<a href="contact.html">Contact</a>
			<a href="privacy.html">Privacy</a>
			<a href="terms.html">Terms</a>
			<a href="delete-data.html">Delete data</a>
		</nav>
	</div>
</footer>
</body>
</html>
"""


def page(name, title, desc, body, current=None, image="assets/gh-feature.jpg"):
    html = head(title, desc, image, "" if name == "index.html" else name) + header(current or name) + "<main>\n" + body + "</main>\n" + FOOTER
    open(os.path.join(OUT, name), "w").write(html)
    print("wrote", name)


GH_TAGS = """<div class="tags">
					<span class="tag live">● IN TESTING</span>
					<span class="tag">ANDROID</span>
					<span class="tag">FREE</span>
					<span class="tag">ARCADE</span>
				</div>"""

# ------------------------------------------------------------------ home
page("index.html", "Neon Afterglow: Indie games that glow",
     "Neon Afterglow makes bright, fast, one-tap games. Our first game, Geometrical Haven, is a neon speed-run for Android.",
     f"""<section class="hero">
	<div class="wrap">
		<div>
			<span class="eyebrow">Independent game studio</span>
			<h1 class="neon"><span class="glow-cyan">Neon</span> <span class="line2 glow-pink">Afterglow</span></h1>
			<p class="lead">Bright, fast, one-tap games you can pick up when you're bored and put down when you're hooked.</p>
			<div class="btns">
				<a class="btn" href="geometrical-haven.html">Play Geometrical Haven</a>
				<a class="btn ghost" href="contact.html">Get in touch</a>
			</div>
		</div>
		<div class="orb"><img src="assets/logo.png" alt="Neon Afterglow logo: a neon ring with a glowing comet around the letters NA"></div>
	</div>
</section>

<section>
	<div class="wrap">
		<span class="eyebrow">Our first game</span>
		<h2 class="neon glow-cyan">Geometrical Haven</h2>
		<div class="panel feature" style="margin-top:24px">
			<a class="art" href="geometrical-haven.html"><img src="assets/gh-feature.jpg" alt="Geometrical Haven: a neon triangle launcher inside an orbit ring, with the ball streaking out"></a>
			<div class="info">
				{GH_TAGS}
				<p>A neon speed-run where every shape moves you differently. Launch from triangles, swing around circles, ride rails and race the clock for gold.</p>
				<div class="btns" style="margin-top:12px">
					<a class="btn pink" href="geometrical-haven.html">See the game</a>
				</div>
			</div>
		</div>
	</div>
</section>

<section>
	<div class="wrap">
		<span class="eyebrow">What we make</span>
		<h2 class="neon glow-pink">Games that glow</h2>
		<div class="cards" style="margin-top:24px">
			<div class="card"><div class="ico">⚡</div><h3>One tap to play</h3><p>Simple controls, instant restarts and short levels, made for quick breaks on your phone.</p></div>
			<div class="card"><div class="ico">🌌</div><h3>Neon everything</h3><p>Glowing shapes, speed trails and synthwave colour, with themes and skins to make it yours.</p></div>
			<div class="card"><div class="ico">🏁</div><h3>Easy to learn, hard to master</h3><p>Anyone can finish a level. Shaving off the last tenth of a second for gold is another story.</p></div>
		</div>
	</div>
</section>

<section>
	<div class="wrap two">
		<div>
			<span class="eyebrow">About</span>
			<h2 class="neon glow-cyan">Who we are</h2>
			<p>Neon Afterglow is a one-person indie studio from Alberta, Canada, run by Chase Pelechytik. Every game is designed, built and tuned by hand, from the physics to the medal times.</p>
		</div>
		<div class="panel">
			<h3 class="glow-gold">🧪 Testers wanted</h3>
			<p style="color:var(--dim)">Geometrical Haven is in closed testing on Google Play. Got an Android phone? Help it launch and play it before anyone else.</p>
			<div class="btns" style="margin-top:12px"><a class="btn" href="contact.html#test">Join the test</a></div>
		</div>
	</div>
</section>
""")

# ------------------------------------------------------------------ games
page("games.html", "Games | Neon Afterglow",
     "All games by Neon Afterglow.",
     f"""<section>
	<div class="wrap">
		<span class="eyebrow">Our games</span>
		<h1 class="neon glow-cyan" style="font-size:clamp(2.2rem,6vw,3.6rem)">Games</h1>
		<p class="lead">One so far, with more on the way.</p>

		<div class="panel feature" style="margin-top:32px">
			<a class="art" href="geometrical-haven.html"><img src="assets/gh-feature.jpg" alt="Geometrical Haven key art"></a>
			<div class="info">
				<h2 class="neon glow-pink" style="font-size:1.8rem">Geometrical Haven</h2>
				{GH_TAGS}
				<p>One-tap neon speed runs. Launch, orbit, ride rails and race for gold medals across 10 handcrafted levels.</p>
				<div class="btns" style="margin-top:12px">
					<a class="btn pink" href="geometrical-haven.html">Learn more</a>
					<a class="btn ghost" href="contact.html#test">Join the test</a>
				</div>
			</div>
		</div>

		<div class="panel" style="margin-top:24px;text-align:center;border-style:dashed">
			<h3 class="neon glow-cyan" style="font-size:1.5rem">Next game: coming soon</h3>
			<p style="color:var(--dim);margin:0">Something new is glowing in the workshop.</p>
		</div>
	</div>
</section>
""")

# ------------------------------------------------------------------ geometrical haven
SHOTS = [("title", "Title screen"), ("gameplay", "Launch from triangles"), ("results", "Race for gold"),
         ("store", "Skins and themes"), ("levels", "10 neon levels")]
shots = "\n".join(f'\t\t\t<figure><img src="assets/shots/{f}.jpg" alt="{c}" loading="lazy" width="540" height="1170"><figcaption>{c}</figcaption></figure>' for f, c in SHOTS)
LEVELS = ["Shape School", "Red Means Dead", "Pick a Lane", "First Climb", "Spin Cycle",
          "Rail Yard", "Bank Shots", "Sludge Run", "Gauntlet", "Overdrive"]
levels = "".join(f"<span>{n}</span>" for n in LEVELS)

page("geometrical-haven.html", "Geometrical Haven | Neon Afterglow",
     "Geometrical Haven: a one-tap neon speed-run game for Android. Launch, orbit, ride rails and race the clock for gold.",
     f"""<section>
	<div class="wrap">
		<div class="game-head">
			<img src="assets/gh-icon.png" alt="Geometrical Haven app icon">
			<div>
				<h1 class="neon glow-cyan" style="font-size:clamp(2rem,6vw,3.4rem);margin:0">Geometrical Haven</h1>
				{GH_TAGS}
			</div>
		</div>
		<p class="lead" style="margin-top:20px">Bored? Race the clock through glowing neon levels in a one-tap speed-run game that's easy to pick up and hard to master. Find the fastest route to the finish, then come back and do it faster.</p>
		<div class="btns">
			<a class="btn pink" href="#play">How to play it</a>
			<a class="btn ghost" href="#features">Features</a>
		</div>
	</div>
</section>

<section>
	<div class="wrap">
		<span class="eyebrow">Screenshots</span>
		<div class="shots" style="margin-top:12px">
{shots}
		</div>
	</div>
</section>

<section id="features">
	<div class="wrap">
		<span class="eyebrow">Shapes that move you</span>
		<h2 class="neon glow-pink">Every shape is a move</h2>
		<div class="cards" style="margin-top:24px">
			<div class="card"><div class="ico">🔺</div><h3>Triangles</h3><p>Snap in, then tap to launch toward your finger.</p></div>
			<div class="card"><div class="ico">⭕</div><h3>Circles</h3><p>Get caught in orbit, tap to reverse, fly off with a speed boost.</p></div>
			<div class="card"><div class="ico">〰️</div><h3>Rails</h3><p>Ride them, build speed, tap to swap sides and dodge hazards.</p></div>
			<div class="card"><div class="ico">⏩</div><h3>Boosts and walls</h3><p>Boost pads fire you forward. Mirror, kicker and bumper walls bounce you around.</p></div>
			<div class="card"><div class="ico">🟣</div><h3>Sludge</h3><p>Slows you right down. Find a way around it.</p></div>
			<div class="card"><div class="ico">🔴</div><h3>Hazards</h3><p>Red means dead. One touch and you restart.</p></div>
		</div>
	</div>
</section>

<section>
	<div class="wrap two">
		<div>
			<span class="eyebrow">What's inside</span>
			<h2 class="neon glow-cyan">Built for speed</h2>
			<ul class="list-check">
				<li><strong>10 handcrafted levels</strong>, each with more than one path</li>
				<li><strong>Bronze, silver and gold</strong> medal times to beat</li>
				<li><strong>27 achievements</strong>, each paying bonus coins</li>
				<li><strong>Skins and themes</strong>: glowing balls with their own trails and sounds, and themes that restyle every level</li>
				<li><strong>Quick sessions</strong>: short levels, instant restarts, plays offline</li>
			</ul>
		</div>
		<div>
			<span class="eyebrow">The levels</span>
			<h2 class="neon glow-gold">From school to overdrive</h2>
			<div class="levels">{levels}</div>
		</div>
	</div>
</section>

<section id="play">
	<div class="wrap">
		<div class="panel">
			<span class="eyebrow">Availability</span>
			<h2 class="neon glow-pink">Coming soon to Google Play</h2>
			<p>Geometrical Haven is in <strong>closed testing</strong> on Google Play right now. You'll need an Android phone and a Google account to join. Send your Gmail address and you'll get the invite link.</p>
			<div class="btns">
				<a class="btn pink" href="contact.html#test">Join the test</a>
			</div>
			<p style="color:var(--dim);font-size:.9rem;margin-top:18px">Free to play with ads. Optional ads give bonus coins. · <a href="privacy.html">Privacy policy</a> · <a href="terms.html">Terms</a> · <a href="delete-data.html">Delete your data</a></p>
		</div>
	</div>
</section>
""", current="games.html")

# ------------------------------------------------------------------ contact
page("contact.html", "Contact | Neon Afterglow",
     "Contact Neon Afterglow: support, testing, press and business.",
     f"""<section>
	<div class="wrap">
		<span class="eyebrow">Say hi</span>
		<h1 class="neon glow-pink" style="font-size:clamp(2.2rem,6vw,3.6rem)">Contact</h1>
		<p class="lead">Questions, bugs, ideas or just your best time on Overdrive: we read everything.</p>

		<div class="panel" style="margin-top:28px">
			<p style="color:var(--dim);margin:0 0 6px">Email</p>
			<a class="contact-big glow-cyan" href="mailto:{EMAIL}">{EMAIL}</a>
			{email_btns("Hello from the website", label="Email us")}
			<p style="color:var(--dim);margin:14px 0 0">We usually reply within a few days.</p>
		</div>

		<div class="cards" style="margin-top:18px">
			<div class="card" id="test">
				<div class="ico">🧪</div><h3>Become a tester</h3>
				<p>Have an Android phone? Email your Gmail address with the subject <strong>"Tester"</strong>, and you'll get the invite link for Geometrical Haven's closed test.</p>
				{email_btns("Tester", "Hi! I'd like to test Geometrical Haven. My Gmail is: ", label="Email to join")}
			</div>
			<div class="card">
				<div class="ico">🐞</div><h3>Support and bugs</h3>
				<p>Tell us your phone model and what happened. A screenshot helps a lot.</p>
				{email_btns("Geometrical Haven support", "Phone model:\nWhat happened:\n", label="Report a bug")}
			</div>
			<div class="card">
				<div class="ico">📰</div><h3>Press and business</h3>
				<p>Writing about the game or want to work together? Get in touch for keys, art and info.</p>
				{email_btns("Press / business", label="Email us")}
			</div>
		</div>
	</div>
</section>

<section>
	<div class="wrap">
		<span class="eyebrow">FAQ</span>
		<h2 class="neon glow-cyan">Quick answers</h2>
		<details><summary>Is Geometrical Haven on iPhone?</summary><p>It's on its way. The Android version comes first, and the iPhone and iPad version is being prepared for the App Store.</p></details>
		<details><summary>Is it free?</summary><p>Yes. It's free to play with ads, and optional ads give you bonus coins.</p></details>
		<details><summary>How do I delete my data?</summary><p>Your progress is stored on your phone: use Settings &gt; Reset All Data in the game, or uninstall it. Leaderboard times are stored online; email us your leaderboard nickname to have them removed. See <a href="delete-data.html">Delete your data</a> for the details.</p></details>
		<details><summary>How do I report an offensive leaderboard name?</summary><p>Email us the nickname and the level it appears on, and we'll review it and remove names that break the <a href="terms.html#leaderboards">rules</a>.</p></details>
		<details><summary>Does the game work offline?</summary><p>Yes. Ads and the world leaderboards just won't show without an internet connection, and your best times upload the next time you're online.</p></details>
	</div>
</section>
""" + COPY_JS)

# ------------------------------------------------------------------ 404
page("404.html", "Lost in the neon | Neon Afterglow", "Page not found.",
     """<section style="text-align:center;padding:120px 0">
	<div class="wrap">
		<h1 class="neon glow-pink" style="font-size:clamp(4rem,14vw,8rem);margin:0">404</h1>
		<p class="lead" style="margin:10px auto 0">Red means dead. This page doesn't exist.</p>
		<div class="btns" style="justify-content:center"><a class="btn" href="index.html">Back to start</a></div>
	</div>
</section>
""", current="")
# GitHub Pages serves 404.html at any missing path, so its links must be absolute.
_p = os.path.join(OUT, "404.html")
_s = open(_p).read()
for _a in ('href="assets/', 'src="assets/', 'href="index.html"', 'href="games.html"', 'href="contact.html"',
           'href="privacy.html"', 'href="terms.html"', 'href="delete-data.html"'):
    _s = _s.replace(_a, _a.replace('="', '="/', 1))
open(_p, "w").write(_s)


# ------------------------------------------------------------------ legal pages
def wrap_legal(name, title):
    """Restyle an existing legal page: keep its content, swap in the site layout."""
    path = os.path.join(OUT, name)
    src = open(path).read()
    if "site-header" in src:          # already wrapped: take the original content back out
        body = re.search(r'<main class="legal">\n(.*)</main>', src, re.S).group(1)
    else:
        body = re.search(r"<body>\n(.*)</body>", src, re.S).group(1)
    html = head(f"{title} | Neon Afterglow", f"{title} for Geometrical Haven by Neon Afterglow.") \
        + header("") + '<main class="legal">\n' + body + "</main>\n" + FOOTER
    open(path, "w").write(html)
    print("restyled", name)


if __name__ == "__main__":
    for n, t in [("privacy.html", "Privacy Policy"), ("terms.html", "Terms of Service"), ("delete-data.html", "Delete Your Data")]:
        if os.path.exists(os.path.join(OUT, n)):
            wrap_legal(n, t)
