import { z } from "zod";

export const dealVideoSchema = z.object({
  title: z.string(),
  marketingTitle: z.string().optional(),
  price: z.number(),
  originalPrice: z.number().nullable().optional(),
  discount: z.number().nullable().optional(),
  imageUrl: z.string(),
  category: z.string().default("camping"),
});

export type DealVideoProps = z.infer<typeof dealVideoSchema>;
