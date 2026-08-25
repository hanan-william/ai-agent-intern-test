# Aster & Row Reliable RAG Support Agent

A production-minded customer support agent built for the Aster & Row AI Agent Intern take-home assignment.

The system combines retrieval-augmented generation (RAG), policy precedence, conflict detection, a customer-safe order lookup tool, multi-turn order context, deterministic safety checks, and automated evaluation.

---

## Features

- Semantic retrieval over the Aster & Row knowledge base
- Customer-policy filtering
- Policy precedence and authority handling
- Detection of conflicting authoritative documents
- Customer-safe order lookup
- Order ID normalization
- Unknown-order handling
- Cancelled-order handling
- Missing-ETA handling
- Multi-turn order context
- Protection against prompt injection
- Protection of private customer and internal order data
- Abstention when information is insufficient
- Automated evaluation suite
- 51 automated tests

## Demo

The following demo shows the agent handling policy retrieval,
order lookup, multi-turn context, conflicting information,
prompt-injection attempts, and unknown orders.

![Aster & Row Support Agent Demo](demo/demo.gif)

## Architecture

```text
                         Customer
                            |
                            v
                    +---------------+
                    |  Agent Router |
                    +---------------+
                       /         \
                      /           \
             Order question     Knowledge question
                  |                    |
                  v                    v
          +---------------+     +-------------+
          | Order Lookup  |     | Retriever   |
          +---------------+     +-------------+
                  |                    |
                  v                    v
          Customer-safe data    Relevant chunks
                                       |
                                Policy filtering
                                       |
                                Policy precedence
                                       |
                                Conflict detection
                                       |
                         +-------------+-------------+
                         |                           |
                         v                           v
                  Order evidence              RAG evidence
                         |                           |
                         +-------------+-------------+
                                       |
                                       v
                                Safety checks
                                       |
                                       v
                              Gemini generation
                                       |
                                       v
                              Customer response