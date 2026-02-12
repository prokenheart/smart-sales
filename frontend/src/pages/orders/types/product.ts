type Price = {
    priceId: string;
    priceAmount: number;
}

export type Product = {
    productId: string;
    productName: string;
    productDescription: string;
    productQuantity: number;
    updatedAt: string;
    prices: Price[];
};