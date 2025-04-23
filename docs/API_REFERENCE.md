# Loomi API Reference

## GraphQL API (Backend)

### Authentication
- `login(email: String!, password: String!): AuthPayload`
- `magicLogin(email: String!): Boolean`
- `verifyMagicLogin(token: String!): AuthPayload`

### Products
- `products(skip: Int, take: Int, where: ProductWhereInput): [Product!]!`
- `product(id: ID!): Product`
- `searchProducts(query: String!): [Product!]!`

### User
- `me: User`
- `updateUser(input: UpdateUserInput!): User`

### Cart
- `myCart: Cart`
- `addToCart(productId: ID!, quantity: Int!): Cart`
- `removeFromCart(productId: ID!): Cart`

### Orders
- `createOrder(input: CreateOrderInput!): Order`
- `myOrders: [Order!]!`

## REST Microservices

### AI Orchestrator (`/api/ai`)
- `POST /chat` - Chat with shopping assistant
- `POST /visual-search` - Search products by image
- `POST /analyze-emotion` - Analyze text sentiment

### Pricing Engine (`/api/pricing`)
- `POST /calculate-price` - Get dynamic price for product
- `POST /bulk-pricing` - Get prices for multiple products
- `GET /market-trends` - Get current market trends

### Supply Chain (`/api/supply`)
- `POST /check-inventory` - Check product inventory
- `POST /estimate-shipping` - Get shipping estimates
- `GET /supply-risks` - Get supply chain risk assessment

## Webhooks

### Stripe
- `POST /webhooks/stripe` - Handle Stripe payment events

### UPI
- `POST /webhooks/upi` - Handle UPI payment notifications