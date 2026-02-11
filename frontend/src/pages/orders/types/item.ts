type Product = {
    productId: string;
    productName: string;
};

export type Item = {
  product: Product;
  itemQuantity: number;
  itemPrice: number;
  orderId: string;
  updatedAt: string;
};
