# Prompt — Build a professional website for **West-Swiss Hotel Aba**

Use the text below as a single, copy-paste prompt to give to a web team, website builder (Wix/WordPress/Shopify/Custom), or an AI site generator. It contains goals, content, page structure, SEO, integrations, design direction, accessibility and acceptance criteria. **Use the provided hotel data** exactly where indicated.

---

**PROJECT SUMMARY / GOAL**
Build a modern, conversion-focused, fully responsive website for **West-Swiss Hotel Aba** that highlights rooms, amenities, location, price comparison (direct vs OTA), and makes it extremely easy for visitors to check availability and book (or compare prices). The site must present trust signals (rating, reviews, policies), strong CTAs, and be optimized for SEO and local search (Aba, Abia).

---

**BRAND / VOICE**
Warm, professional, hospitality-first. Clear, concise copy that sells comfort, value and convenience. Emphasize serenity (restaurant), accessibility, free inclusions (Wi-Fi, breakfast, parking), and family/business friendly features.

---

**CORE HOTEL DATA (use verbatim where relevant)**

* Name: **West-Swiss Hotel Aba**
* Google rating summary: **4.4 (101 reviews)**
* Address: **23A Margaret Avenue, GRA, Aba 450101, Abia**
* Plus Code: **49H9+6M Aba**
* Check-in: **14:00** | Check-out: **12:00**
* Amenities (highlight): **Free Wi-Fi, Free breakfast, Free parking, Accessible, Pool, Air-conditioned**
* Nearby neighborhood: **Aba** — "Great for visitors (3.9 based on sightseeing, recreation, and getting around)"
* Review highlight (use as testimonial): *"West Swiss Hotel's restaurant is so serene and neatly set up. No noise, just ease the stress while eating..."*
* Pricing examples / competitor quotes to show in price comparison widget:

  * Official site: **₦80,500**
  * Expedia.com: **₦114,162** (Free breakfast · Free Wi-Fi · Free parking)
  * ZenHotels.com: **₦126,831** (Free breakfast)
  * Hotels.ng: **₦112,750**
  * Bluepillow.com: **₦114,162** (Free cancellation until 8 Feb)

---

## Deliverables (what to build)

1. **Homepage** — Hero with booking/search bar, short benefits, rating badge, price comparison teaser, quick links to Rooms, Amenities, Restaurant, Gallery, Contact.
2. **Rooms & Rates** — Room types, key features, gallery per room, rate table, booking CTA. Include dynamic price comparison (pull OTA rates or show manual comparison block).
3. **Dining & Restaurant** — Short description, sample menu highlights, serenity statement, restaurant hours.
4. **Amenities** — Visual icons + short bullets for: Free Wi-Fi, Free breakfast, Free parking, Accessible, Pool, Air-conditioned, etc.
5. **Location & Things to Do** — Map embed (Google Maps using address/plus code), nearby attractions, transport info.
6. **Reviews & Testimonials** — Display aggregated rating (4.4/101), selected guest quotes, link to full reviews.
7. **Gallery** — High-quality images: rooms, pool, restaurant, exterior, public spaces. Lightbox viewer.
8. **Contact & Booking** — Contact form, phone link, email, reservation form, availability calendar. Show check-in/out policy.
9. **Policies & FAQs** — Check-in/out times, cancellation, parking, pets, accessibility.
10. **Footer** — Address, phone, email, social links, copyright, small site map, privacy policy link.
11. **Admin/CMS** — Ability to update rates, pages, images, and publish special offers.
12. **Sitemap & Robots** — Auto-generated sitemap.xml and robots.txt.

---

## Page-by-page content (copy examples to use)

**Homepage Hero (headline + subheadline + CTA):**
Headline: *Comfort & Convenience in the Heart of Aba*
Subheadline: *4.4★ | Free Wi-Fi • Free breakfast • Free parking — Book direct from ₦80,500 or compare prices.*
Primary CTA: **Check availability** (opens booking widget / calendar)
Secondary CTA: **Compare prices**

**About (short):**
West-Swiss Hotel Aba offers comfortable, air-conditioned rooms and friendly service at 23A Margaret Avenue, GRA, Aba. Ideal for leisure and business travellers — enjoy free breakfast, complimentary Wi-Fi and on-site parking. Our serene on-site restaurant is a guest favourite.

**Rooms intro:**
Choose from well-appointed standard and deluxe rooms with pool or city views. All rooms include air conditioning, free Wi-Fi, and complimentary breakfast.

**Restaurant blurb (use review line):**
Our restaurant provides a calm, neatly set dining experience — "No noise, just ease the stress while eating..." Enjoy local and international dishes prepared fresh each day.

**Contact block:**
Address: 23A Margaret Avenue, GRA, Aba 450101, Abia
Phone: *[Add hotel phone]* (display prominently)
Check-in: 14:00 | Check-out: 12:00

---

## Design & UI Guidance

* Visual style: modern, warm neutrals with one accent color (deep teal or warm orange). Clean typography, large hero image.
* Layout: mobile-first, responsive grid, sticky top navigation on scroll.
* Imagery: professional photography, real rooms and restaurant. Use lightbox for gallery.
* Trust badges: 4.4/101 rating badge, secure booking (HTTPS), third-party OTA logos in price comparison.
* Buttons: clear CTAs — primary color for “Check availability / Book”, secondary for “Compare prices / Contact”.
* Accessibility: WCAG AA color contrasts, keyboard navigable, alt text for all images.

---

## Technical / Integrations

* **Booking:** integrate with the existing booking engine if available (direct booking) OR connect to a third-party booking widget (Booking.com/Expedia/widget) and ensure availability calendar sync (or show price comparison if full sync not possible).
* **Price comparison widget:** show official site rate (₦80,500) and OTA rates (Expedia ₦114,162; ZenHotels ₦126,831; Hotels.ng ₦112,750; Bluepillow ₦114,162). If live API access is unavailable, create an editable admin table for manual rate updates.
* **Maps:** embed Google Maps using address/plus code 49H9+6M Aba.
* **Analytics:** GA4 + Google Search Console.
* **SEO:** server-side rendering or pre-rendered meta tags; schema.org Hotel structured data (Hotel & LocalBusiness).
* **Performance:** Lighthouse score target: **90+** on desktop, **≥80** on mobile. Page load < 2s on 4G.
* **Security:** HTTPS, form spam protection (reCAPTCHA v3 or alternative).
* **Privacy & Compliance:** cookie banner, privacy policy, contact opt-in.
* **Accessibility:** WCAG AA compliance, semantic HTML, skip links.

---

## SEO / Metadata (examples to implement)

* **Homepage title:** West-Swiss Hotel Aba — Comfortable Rooms & Free Breakfast in Aba
* **Homepage meta description:** Stay at West-Swiss Hotel Aba (4.4★, 101 reviews). Convenient location in GRA Aba, free Wi-Fi, free breakfast, pool and parking. Book direct from ₦80,500 or compare prices.
* **Primary keywords:** Aba hotel, hotels in Aba, West Swiss Hotel Aba, Aba accommodation, hotels near GRA Aba.
* **Local SEO:** Add structured data (LocalBusiness/Hotel), create Google Business Profile link, embed plus code. Include NAP (name, address, phone) on every page.

---

## Structured Data (developer note)

Add `Hotel` schema with: name, address, geo/plus code, telephone, priceRange, aggregateRating (4.4, reviewCount 101), amenities (amenityFeature).

---

## Admin & Content Requirements

* Easy CMS editing for: hero copy, room descriptions, rates, gallery photos, restaurant menu, FAQs, policies.
* Editable price comparison table.
* Contact form submissions saved to admin and emailed to reservations.
* Exportable bookings/guest inquiries (CSV).

---

## Acceptance Criteria (QA checklist)

* Responsive across devices (mobile, tablet, desktop).
* Booking CTA and availability calendar visible & working.
* Price comparison shows official and OTA rates as provided.
* Google Maps embed shows the correct address/plus code.
* Pages have meta titles and descriptions and basic schema.
* Images optimized for web with descriptive alt text.
* Site passes basic accessibility checks (keyboard nav, contrast).
* Analytics events for booking clicks, contact submissions, and price-compare clicks.
* Content uses the supplied facts and the exact review quote shown above.

---

## Optional / Nice-to-have features

* Live chat or WhatsApp booking button.
* Special offers/seasonal promo banner (editable).
* Multi-language toggle (English + Igbo / Nigerian English).
* Rates calendar with minimum stay rules.
* Printable PDF of room brochure.

---

## Files & Assets to provide to developer (if available)

* High-resolution photos (rooms, pool, restaurant, exterior → ideally 1920px wide)
* Logo (SVG + PNG)
* Any existing booking engine API credentials or OTA partner details.
* Hotel contact phone and email (to be inserted where placeholder exists).
* Restaurant menu PDF (if available).

---

## Final notes for implementer

Please use the hotel data provided above verbatim where indicated. Prioritize a fast path to launch: a one-page MVP with booking + price comparison is acceptable first, but code and CMS should support quick expansion to the full page set. Hand over documentation for updating rates, images, and offers.

---
