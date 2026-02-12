type Product = {
    productId: string;
    productName: string;
};

export type Item = {
  product: Product;
  itemQuantity: number;
  itemPrice: number;
  orderId: string | undefined;
  updatedAt: string | undefined;
};

export type ItemPost = {
  productId: string;
  itemQuantity: number;
}
