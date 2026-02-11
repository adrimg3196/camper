import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { Background } from "../../components/Background";
import { ProductImage } from "../../components/ProductImage";
import { PriceDisplay } from "../../components/PriceDisplay";
import { TitleReveal } from "../../components/TitleReveal";
import { CallToAction } from "../../components/CallToAction";
import { Watermark } from "../../components/Watermark";
import { DialogueSubtitles } from "../../components/DialogueSubtitles";
import { dealVideoSchema, type DealVideoProps } from "./schema";
import "../../styles/global.css";

export const DealVideoSchema = dealVideoSchema;

export const DealVideo: React.FC<DealVideoProps> = (props) => {
  const { fps } = useVideoConfig();
  const displayTitle = props.marketingTitle || props.title;

  // Determinar si tenemos audio TTS
  const hasAudio = !!props.audioFile;
  const hasDialogue = props.dialogueSegments && props.dialogueSegments.length > 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      {/* Layer 0: Animated gradient background (always) */}
      <Background category={props.category} />

      {/* Layer 1: Product image with zoom reveal (from 0.5s - más rápido con audio) */}
      {/* Cuando hay diálogo, el producto se anima como si "hablara" */}
      <Sequence from={Math.round(fps * 0.5)} name="ProductImage">
        <ProductImage imageUrl={props.imageUrl} isAnimated={hasDialogue} />
      </Sequence>

      {/* Layer 2: Title text - solo si NO hay diálogo (el diálogo reemplaza el título) */}
      {!hasDialogue && (
        <Sequence from={Math.round(fps * 1.5)} name="Title">
          <TitleReveal text={displayTitle} />
        </Sequence>
      )}

      {/* Layer 3: Dialogue subtitles - animados y sincronizados con audio */}
      {hasDialogue && (
        <DialogueSubtitles segments={props.dialogueSegments!} />
      )}

      {/* Layer 4: Price + discount (aparece durante el diálogo de precio) */}
      <Sequence from={Math.round(fps * 5)} name="Price">
        <PriceDisplay
          price={props.price}
          originalPrice={props.originalPrice}
          discount={props.discount}
        />
      </Sequence>

      {/* Layer 5: Call to action + affiliate link (from 9s - sincronizado con CTA del diálogo) */}
      <Sequence from={Math.round(fps * 9)} name="CTA">
        <CallToAction affiliateUrl={props.affiliateUrl} />
      </Sequence>

      {/* Layer 6: Persistent watermark (always) */}
      <Watermark />

      {/* Audio track: TTS voice o silencio */}
      {hasAudio ? (
        <Audio src={staticFile(props.audioFile!)} volume={1} />
      ) : (
        <Audio src={staticFile("silence.mp3")} volume={0} />
      )}
    </AbsoluteFill>
  );
};
