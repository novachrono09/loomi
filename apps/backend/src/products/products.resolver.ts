import { Resolver, Query, Mutation, Args } from '@nestjs/graphql';
import { ProductsService } from './products.service';
import { Product } from '../@generated/product/product.model';
import { ProductCreateInput } from '../@generated/product/product-create.input';
import { ProductWhereUniqueInput } from '../@generated/product/product-where-unique.input';
import { ProductUpdateInput } from '../@generated/product/product-update.input';

@Resolver(() => Product)
export class ProductsResolver {
  constructor(private readonly productsService: ProductsService) {}

  @Query(() => [Product])
  async products(
    @Args('skip', { nullable: true }) skip?: number,
    @Args('take', { nullable: true }) take?: number,
    @Args('where', { nullable: true }) where?: any,
    @Args('orderBy', { nullable: true }) orderBy?: any,
  ) {
    return this.productsService.products({
      skip,
      take,
      where,
      orderBy,
    });
  }

  @Query(() => Product, { nullable: true })
  async product(@Args('where') where: ProductWhereUniqueInput) {
    return this.productsService.product(where);
  }

  @Mutation(() => Product)
  async createProduct(@Args('data') data: ProductCreateInput) {
    return this.productsService.createProduct(data);
  }

  @Mutation(() => Product)
  async updateProduct(
    @Args('where') where: ProductWhereUniqueInput,
    @Args('data') data: ProductUpdateInput,
  ) {
    return this.productsService.updateProduct({ where, data });
  }

  @Mutation(() => Product)
  async deleteProduct(@Args('where') where: ProductWhereUniqueInput) {
    return this.productsService.deleteProduct(where);
  }

  @Query(() => [Product])
  async searchProducts(@Args('query') query: string) {
    return this.productsService.searchProducts(query);
  }
}