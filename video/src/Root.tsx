import React from "react";
import { Composition } from "remotion";
import { DealVideo, DealVideoSchema } from "./compositions/DealVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="DealVideo"
      component={DealVideo}
      durationInFrames={450}
      fps={30}
      width={1080}
      height={1920}
      schema={DealVideoSchema}
      defaultProps={{
        title: "Lixada Estufa de Camping Gas Portatil",
        marketingTitle: "Estufa PRO para aventureros",
        price: 18.99,
        originalPrice: 25.99,
        discount: 27,
        imageUrl: "https://m.media-amazon.com/images/I/71RJn7QLZAL._AC_SL1500_.jpg",
        category: "cocina-camping",
      }}
    />
  );
};
