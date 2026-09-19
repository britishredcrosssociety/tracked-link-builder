# Issue 62 – "Final URL suffix" for cpc mediums (Paid Search / Performance Max / Demand Gen)

BRC runs donation campaigns on Google Ads and Microsoft (Bing) Ads – across three
campaign types: classic paid search, Performance Max and Demand Gen. Both platforms **auto-tag** clicks, which covers the standard Google Analytics `utm_*` parameters, so until now the link builder had no notion of Performance Max or Demand Gen at all.

BRC requires additional tracking parameters to be present in the URL – the `c_*` family (`c_name`, `c_source`, `c_medium`, as far as we understand, they are what the donate platform and the downstream fundraising reporting use to attribute a donation to a campaign, an appeal and a creative.

### Implementation Overview

This implementation now allows the link builder to produce a **Final URL suffix** – a bare string of `c_*` parameters such as

```text
c_medium=cpc&c_source=google&c_name=General%20Fund%20Appeal&c_id={campaignid}&adg=brand&c_creative=phrase
```

that the user pastes, unchanged, into the campaign's _Final URL suffix_ setting in Google Ads or Microsoft Ads. The ad platform appends it to every landing page URL of that campaign and fills in the `{campaignid}` / `{CampaignId}` placeholder itself, so every click carries a consistent, taxonomy-compliant set of BRC parameters alongside the auto-tagged `utm_*` ones. All values are produced from dropdowns (the existing appeal list plus a handful of new ones), which is what gives the consistency the reporting needs.

Everything else in the tool, that is every other medium, its inputs and its tracked-link output, is unchanged.

### Changes in the UI

**1\. "What are you making a tracked link for?" (the medium dropdown)**

*   _Paid search_ is still there, relabelled **"Paid search (Google Ads / Microsoft Ads)"**, and now leads to a working

path instead of a refusal message.

*   Two new options: **"Performance Max (Google Ads / Microsoft Ads)"** and **"Demand Gen (Google Ads)"**.

**2\. When one of those three is selected**

The red "this tool isn't for paid search" warning is replaced by a short explanation of why a suffix is produced instead of a link, and the form changes shape:

*   Hidden (not relevant to a suffix): _What BRC site page are you linking to?_, Does this tracked link need

individual-level tracking added?, the marketing objective and the taxonomy source code.

*   Kept: **What area of BRC work does the link relate to?** (the appeal dropdown) – this becomes `c_name`.
*   New inputs: The medium itself becomes `c_medium` = `cpc`, `performance-max` or `demand-gen`.

**3\. Section "2) Copy and Paste"**

The previous "Code to use" box is replaced by a **"Final URL suffix to use"** box, followed by a note telling the user where to paste it in the ad platform and not to edit the `{campaignid}` part. The GA4 reference table below it shows "TBC" for these mediums, as there is no `utm_*` output to describe. Switching back to any other medium restores the normal form and output.

**4\. A small usability fix that benefits every medium**

Choosing an appeal in _What area of BRC work does the link relate to?_ (and an audience in the Paid Social multi-selects) now refreshes the output immediately. Previously the output only updated on the next interaction with another field – a long-standing quirk that became obvious once the suffix path had so few other fields to touch.

## Technical Details

Google Ads and Microsoft (Bing) Ads auto-tag the `utm_*` parameters, so a full tracked link is not needed, but the `c_*` parameters are not auto-tagged. For the three cpc mediums the link builder now produces a **Final URL suffix** (a bare query-string fragment, no domain, no `?`, no `utm_*`) that the user pastes into the campaign's "Final URL suffix" setting in the ad platform.

Output shape (parameter order follows the prototype tabs in the spec):

```text
c_medium=<cpc|performance-max|demand-gen>&c_source=<google|bing>&c_name=<appeal>&c_id=<{campaignid}|{CampaignId}>
  + Paid Search:                  &adg=<generic|brand|mixed>&c_creative=<exact|phrase|broad|mixed>
  + Performance Max / Demand Gen: &adg=<acquisition|retention>
  + optional:                     &c_code=<source code, max 6 alphanumeric chars>
```

Examples:

| Inputs | Suffix |
| ---| --- |
| Paid Search · Bing · generic · mixed · Gaza Crisis Appeal | `c_medium=cpc&c_source=bing&c_name=Gaza%20Crisis%20Appeal&c_id={CampaignId}&adg=generic&c_creative=mixed` |
| Paid Search · Google · brand · phrase · General Fund Appeal | `c_medium=cpc&c_source=google&c_name=General%20Fund%20Appeal&c_id={campaignid}&adg=brand&c_creative=phrase` |
| Performance Max · Bing · acquisition · Gaza Crisis Appeal | `c_medium=performance-max&c_source=bing&c_name=Gaza%20Crisis%20Appeal&c_id={CampaignId}&adg=acquisition` |
| Demand Gen · Google · acquisition · General Fund Appeal | `c_medium=demand-gen&c_source=google&c_name=General%20Fund%20Appeal&c_id={campaignid}&adg=acquisition` |

## Decisions

*   **All values lowercase** (`cpc`, `performance-max`, `demand-gen`, `google`, `bing`, and the adg / c\_creative option values). `c_name` keeps the appeal name's own casing, e.g. `General%20Fund%20Appeal`. (The spec's prototype tabs used mixed case; the "Expected output" line used lowercase – lowercase was chosen.)
*   **`c_id`** **is a placeholder**, never typed by the user: `{campaignid}` for Google, `{CampaignId}` for Bing. The taxonomy code / marketing objective block (`#taxonomy`) is therefore hidden for these mediums.
*   **The suffix is always generated** – it is not gated on the marketing objective being a "donation" one.
*   **Targeting type** for Performance Max / Demand Gen offers `acquisition` (default) and `retention`.
*   **Optional source code** (→ `c_code=`) is offered for all three mediums; only appended when filled in.
*   `Demand-Gen-` (trailing hyphen in the prototype) was treated as a typo → `demand-gen`.
*   The **domain** and **"individual-level tracking?"** questions are hidden for these mediums: the suffix never contains the domain, and `c_*` parameters _are_ the individual-level tracking, so both would only confuse.
## Where the code changed (all in `index.html`, every block wrapped in inline comments)

| Area | What |
| ---| --- |
| `#medium` options | "Paid Search" relabelled; `Performance Max` and `Demand Gen` options added. |
| `#mediumPPCSearch` | The old "this tool isn't for paid search" alert is repurposed as guidance (id kept – every `toggleFields()` branch hides it). |
| `#mediumPaidSearch` (new div after `#taxonomy`) | `#paidsearchsource`, `#mediumPaidSearchKeyword` (`#paidsearchkeywordstrategy`, `#paidsearchmatchtype`), `#mediumPaidSearchTargeting` (`#paidsearchtargetingtype`), `#paidsearchsourcecode`. Follows the `<prefix><field>` id convention. |
| `div.output` | New `.showSuffixBox` elements: `textarea#urlsuffix` + `#suffixHelp`. |
| `var CPC_MEDIUMS` (top of first script) | Global map `#medium value → c_medium value`; a truthy lookup is the "is cpc medium?" test. |
| `toggleFields()` | 4-line pre-reset at the top (hide `#mediumPaidSearch` / `.showSuffixBox`, show domain + isIndividual paragraphs) so the other 32 branches did not need editing. The old Paid Search branch now matches all three cpc mediums and shows/hides the new elements; `#urlHidden` is hidden (it used to be shown). |
| `updateOutput()` | Early `if (CPC_MEDIUMS[medium]) { updateSuffixOutput(medium); return; }` right after `medium` is read. |
| `updateSuffixOutput(medium)` (new, before `get_elements()`) | Builds the suffix, writes it to `#urlsuffix`, clears `#url`, resets the GA4 table cells to `TBC`. |
| `initpage()` | New delegated click handler on `.dropdown-single, .dropdown-multiple-label` for `li[tabindex], .del, .dropdown-clear-all` → `setTimeout(updateOutput, 0)`. Fixes a pre-existing issue where choosing a campaign (appeal) or a Paid Social audience did not refresh the output until the next interaction (see below). |

### Why a separate output element and an early return

*   The `#url` sanitiser in `updateOutput()` strips `{` `}` (and `%7B` `%7D`), which would destroy the `{campaignid}` placeholder.
*   `get_elements()` calls `new URL()` on the first line of `#url`; a bare suffix is not a URL and would throw.
*   `automated_checks.py` / `url_validation.py` only scrape `textarea#url`, so they are unaffected (and, per project rules, were not modified).
*   The appeal name gets the _same_ character clean-up as the normal link (same regexes as the `#url` sanitiser, plus dot removal), applied before the placeholder is concatenated.
*   **Gotcha found in testing:** `#url` must be cleared with `.html('')` (as `updateOutput()` writes it), not `.val('')`. Setting `.value` directly marks the textarea "dirty", after which the `.html()` writes no longer show – the normal link would have appeared blank after visiting a cpc medium. `#urlsuffix` is written with `.val()` consistently, so it has no such issue.

### Code style

ES5 only to ensure compatibility (`var`, function declarations, string concatenation); jQuery 1.11 API (`.toggle(bool)`, `.closest()`, `.val()`). No new event listeners were needed: the new selects/inputs are static HTML so `initpage()`'s `$('select').change` /
`$('input').keyup|click` bindings pick them up, and sub-block visibility depends only on `#medium`, which already calls `toggleFields()`.

## Suggested Test Path

1. Medium = Paid search → domain, individual-level question, taxonomy block hidden; platform + keyword strategy + match type + source code shown; targeting type hidden; suffix box shown; normal URL box and "no tracked link" alert hidden.
2. Medium = Performance Max / Demand Gen → as above but targeting type shown, keyword strategy + match type hidden.
3. Reproduce the examples table above.
4. Source code `12-3456` → `&c_code=123456` (non-alphanumerics dropped); clear it → parameter gone.
5. Switch back to Banner / Email / Referral / Organic search → suffix elements gone, domain + individual question back, normal output and GA4 table unchanged (Banner output compared against `checks/generated_urls.json['banner'][0]`).