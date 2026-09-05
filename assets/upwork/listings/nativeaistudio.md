# Upwork listing copy — AI chat feature in an iOS app

Paste-ready. Field names match the Upwork "Create a project" form.
Cards to upload: `assets/upwork/cards/nativeaistudio/01-hero.png` … `06-fit.png` (`01-hero` becomes the thumbnail).

This is the differentiated listing. Almost nobody on Upwork sells *native iOS* AI integration by someone who has shipped both. Publish it even if it sells slowly — it is the one that gets you found.

---

## Category

Development & IT → Mobile Development → iOS Development
(secondary fit: AI & Machine Learning → AI Integration)

## Search tags / skills (pick 5)

`SwiftUI` · `iOS Development` · `AI Integration` · `OpenAI API` · `Swift`

## Title

> I will add an AI chat feature to your iOS app with Claude or GPT

Alternates:
- I will build a streaming AI assistant into your SwiftUI app
- I will integrate the Claude or OpenAI API into your iOS app

## Description

I add AI features to iOS apps — streaming chat, assistants, tool calling — built native in SwiftUI against the Claude or OpenAI API.

Most "AI in your app" builds fail in the same three places. The stream stutters or dies halfway. The API key ships inside the binary where anyone can pull it. And nobody costs the thing out until the first invoice arrives. I build the transport layer first, keep the key off the device, and hand you a number for what each conversation costs.

Eleven years of iOS, most of it in banking inside global financial firms, plus daily work with the Claude Agent SDK and MCP.

**What you get**

- Streaming responses, token by token — no spinner, no freeze
- Tool use / function calling wired to your app's own data
- Conversation history persisted with SwiftData
- API key handled server-side or in Keychain, never hardcoded
- Cancel, retry and rate-limit handling that actually works
- Markdown and code-block rendering in the chat bubble
- Prompt caching to cut your per-call token cost
- A Loom walkthrough of the model calls and the cost model

**How it runs**

Day 0 you send repo access, your API provider, and what the AI should be able to do. Day 2 the streaming client, error handling and cancellation are done — the hard part, early. By day 5 the chat UI, history and tool calls are wired to your data and you get a build to try. At handoff we review cost, tune prompts, run your revision round, and I flag what to watch in production.

**About the screenshots**

The screens shown are from NativeAIStudio, a reference app I designed and built myself to demonstrate this exact stack. It is not client work — it is the standard your build is held to.

## Tiers

| | Starter | Standard | Premium |
|---|---|---|---|
| Price | $499 | $1,400 | $3,000 |
| Delivery | 7 days | 14 days | 24 days |
| Revisions | 1 | 2 | 3 |
| Streaming chat screen | ✓ | ✓ | ✓ |
| Keychain key storage | ✓ | ✓ | ✓ |
| Conversation history (SwiftData) | – | ✓ | ✓ |
| Tool calling on your data | – | ✓ | ✓ |
| Markdown + code rendering | – | ✓ | ✓ |
| Cancel, retry, rate limits | – | ✓ | ✓ |
| Multi-turn agent with tool loop | – | – | ✓ |
| Prompt caching + cost breakdown | – | – | ✓ |
| Proxy endpoint so no key ships | – | – | ✓ |
| Unit tests on the model layer | – | – | ✓ |
| Source code | ✓ | ✓ | ✓ |

## Add-ons (optional extras)

- Extra tool / function wired to your data — $180, +2 days
- Voice input with on-device speech-to-text — $260, +3 days
- Streaming proxy endpoint deployed for you — $400, +4 days
- Swap providers later (Claude ↔ OpenAI ↔ Gemini) — $200, +2 days
- Token usage dashboard inside the app — $240, +3 days

## FAQ

**Which model providers do you support?**
Claude (Anthropic), OpenAI, and Gemini. I default to Claude unless you have a reason to prefer another. Swapping later is an add-on, not a rebuild — the model layer is behind a protocol.

**Do I need my own API key?**
Yes. You keep the account and the billing. I never put my key in your app.

**Is my key safe in the app?**
Keychain on Starter and Standard, which is fine for internal or single-user apps. For a public App Store app you want the Premium tier's proxy so the key never leaves your server.

**What will it cost me to run?**
Depends on your model and message length. At handoff you get a per-conversation estimate and prompt caching configured, which typically cuts repeat-context cost sharply. I show you the arithmetic, not a guess.

**Can the AI use my app's data?**
Yes — that is tool calling, included from the Standard tier. You tell me what functions to expose, I wire them to the model.

**Will Apple approve an AI feature?**
They approve them routinely. The usual rejections are missing content moderation and no way to report objectionable output. I include both patterns.

**Do you fine-tune models or run inference on-device?**
No. This is API integration. On-device Core ML or fine-tuning is a different project — message me and I will refer you or quote it separately.

**Can you work on my existing app?**
Yes, that is the normal case. Send repo access at kickoff. UIKit apps are fine; I bridge SwiftUI in through `UIHostingController`.

## Requirements from buyer (mark all mandatory)

1. What should the AI do inside your app? Two or three sentences.
2. Repo access, or a zip of the Xcode project.
3. Which provider do you want — Claude, OpenAI, or Gemini? Do you already have an API key?
4. Should the AI read or act on your app's data? If yes, which data?
5. Minimum iOS version you must support.
6. Is this app already on the App Store, or pre-launch?
7. Roughly how many users and messages per day do you expect? (Drives the cost model.)
8. Any deadline I should know about.

## Project steps (workroom checklist)

Steps 1 and 2 are Upwork's own bookends. These are the ones you add in between. Tick each in the
workroom as it lands — same list for all three tiers.

1. **Requirements locked**
   You send repo access, your API provider and key, and what the AI should be able to do. The
   delivery clock starts once this is complete.
2. **Transport layer**
   Streaming client, error handling, retries and cancellation land first — the hard part, done
   early. You get a build that talks to the model.
3. **Chat surface built**
   Chat UI, message history, markdown and code-block rendering, and tool calls wired to your
   app's data. Pushed to your repo daily.
4. **Cost and prompt tuning**
   Prompt caching turned on, token usage measured, and a written cost-per-user estimate.
5. **Walkthrough delivered**
   Loom video of the model calls, the cost model, and what to watch in production.
6. **Revision round**
   You review and send one consolidated list of changes. I fix, you confirm, we close.
