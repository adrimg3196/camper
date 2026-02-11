import { z } from "zod";

// Segmento de diálogo con timing
const dialogueSegmentSchema = z.object({
  start: z.number(), // segundos desde inicio
  end: z.number(),   // segundos desde inicio
  text: z.string(),  // texto del diálogo
});

export const dealVideoSchema = z.object({
  title: z.string(),
  marketingTitle: z.string().optional(),
  price: z.number(),
  originalPrice: z.number().nullable().optional(),
  discount: z.number().nullable().optional(),
  imageUrl: z.string(),
  category: z.string().default("camping"),
  affiliateUrl: z.string().optional(),
  // Nuevos campos para audio/diálogo
  audioFile: z.string().optional(),           // nombre del archivo de audio TTS
  dialogueSegments: z.array(dialogueSegmentSchema).optional(), // segmentos para subtítulos
});

export type DealVideoProps = z.infer<typeof dealVideoSchema>;
export type DialogueSegment = z.infer<typeof dialogueSegmentSchema>;
