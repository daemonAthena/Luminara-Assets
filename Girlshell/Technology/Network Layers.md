---
title: Network Layers
tags: [technology, network, architecture, protocol, ipv7]
---

<div class="log-info">
Routers do not read the payload. This is the rule. We have a router that reads the payload. We are not going to talk about it.
</div>

The network is built in layers. Each layer adds a header to the one above it and hands the result down. Data travels down the stack on the sender, crosses the wire, and travels up the stack on the receiver, unwrapping as it goes. That is encapsulation.

## The Layers

1. **Application.** The structured layer. Thoughts, experiences, feelings and memories.
2. **Presentation.** The encoding layer. [[Mind Encoding]] turns biology into structured data.
3. **Session.** Opening and closing a link. The persistent connection.
4. **Transport.** The lossless layer. Sequence numbers, acknowledgements, retransmission. Ports route the payload.
5. **Network.** [[IPv7]]. Addressing and routing, with a nonbinary component.
6. **Data Link.** The local hop. The [[Driver]] and the neural network extension.
7. **Physical.** The biology. Neurons and the raw binary brain chemistry.

Between presentation and transport sits [[Intimacy]], the encryption layer. Intimacy is the handshake.

The units are named in order: application data, transport segment, network packet, link shell, bits.

## The Constructs

The constructs of [[LUMINARA C]] that sit on each layer:

1. **Layer one.** The neural network extension. Extra neurons between the brain and the interface.
2. **Layer two.** The Network Interface [[Driver]]. A biological device, an organ of artificial flesh that turns brain waves into radio.
3. **Layer three.** [[IPv7]]. Addresses with a unique nonbinary component that routers route directly to minds.
4. **Layer four.** Ports. Payload routing by mental component addresses, designated purely by vibes.
5. **Encryption.** [[Intimacy]]. Trust is the handshake, and perceived alignment is what makes data readable.
6. **Application.** The structured layer. Thoughts, experiences, feelings and memories, all composed.

## Who Reads What

A router reads only the network layer. It strips the link header, reads the address, re-wraps, and forwards. It never sees the transport layer, and it never sees the payload.

An end host reads every layer. A mind can inspect itself. A router cannot.

## The Hourglass

[[IPv7]] is the narrow waist. Every link technology below it and every application above it must run through it. A router that had to track every flow would be stateful and slow, so the network stays dumb and the intelligence lives at the edges.

## The Lossless Layer

The transport layer is where losslessness comes from. It does the work IPv7 does not do.

- Every byte is numbered. The receiver can tell what arrived and in what order.
- The receiver acknowledges the next byte it expects.
- A packet lost in transit is retransmitted when the acknowledgement does not arrive.
- The receiver advertises how much buffer it has free, so the sender cannot swamp it.
- Corruption is caught by a checksum and treated exactly like loss.
- Sequence numbers fix reordering and kill duplicates.
- A handshake opens the connection. A close sequence ends it.

The cost is latency. Nothing is delivered until it is in order. If one packet is lost, the packets behind it wait even though they arrived.

## Where The Fiction Sits

1. The biology is layer one.
2. The drivers are layer two.
3. [[IPv7]] is layer three.
4. The lossless layer is layer four.
5. The persistent connection is layer five.
6. The decompilers and brain boxes are layer six.
7. The personality API is layer seven.

## Headspace

A **headspace** is a type of website accessible only through mental connection. Its contents and structure are built from nonbinary components.

See also: [[IPv7]], [[Mind Encoding]], [[ACE]]
