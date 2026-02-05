import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { Background } from "../../components/Background";
import { ProductImage } from "../../components/ProductImage";
import { PriceDisplay } from "../../components/PriceDisplay";
import { TitleReveal } from "../../components/TitleReveal";
import { CallToAction } from "../../components/CallToAction";
import { Watermark } from "../../components/Watermark";
import { dealVideoSchema, type DealVideoProps } from "./schema";
import "../../styles/global.css";

export const DealVideoSchema = dealVideoSchema;

export const DealVideo: React.FC<DealVideoProps> = (props) => {
  const { fps } = useVideoConfig();
  const displayTitle = props.marketingTitle || props.title;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0a0a0a" }}>
      {/* Layer 0: Animated gradient background (always) */}
      <Background category={props.category} />

      {/* Layer 1: Product image with zoom reveal (from 1s) */}
      <Sequence from={Math.round(fps * 1)} name="ProductImage">
        <ProductImage imageUrl={props.imageUrl} />
      </Sequence>

      {/* Layer 2: Title text (from 1.5s) */}
      <Sequence from={Math.round(fps * 1.5)} name="Title">
        <TitleReveal text={displayTitle} />
      </Sequence>

      {/* Layer 3: Price + discount (from 5s) */}
      <Sequence from={Math.round(fps * 5)} name="Price">
        <PriceDisplay
          price={props.price}
          originalPrice={props.originalPrice}
          discount={props.discount}
        />
      </Sequence>

      {/* Layer 4: Call to action (from 10s) */}
      <Sequence from={Math.round(fps * 10)} name="CTA">
        <CallToAction />
      </Sequence>

      {/* Layer 5: Persistent watermark (always) */}
      <Watermark />

      {/* Silent audio track (TikTok requires audio) */}
      <Audio src={staticFile("silence.mp3")} volume={0} />
    </AbsoluteFill>
  );
};
