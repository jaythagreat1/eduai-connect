import React from "react";
import styled from "styled-components";
import Navbar from "./Navbar";

const Section = styled.div`
  height: 100vh;
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  position: relative;

  @media (max-width: 768px) {
    scroll-snap-align: none;
    min-height: 100vh;
  }
`;

const Container = styled.div`
  height: 100%;
  scroll-snap-align: center;
  width: 1400px;
  display: flex;
  justify-content: space-between;

  @media (max-width: 1400px) {
    width: 100%;
    padding: 0 20px;
  }

  @media (max-width: 768px) {
    width: 100%;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
    padding: 80px 20px 20px;
  }
`;

const Left = styled.div`
  flex: 2;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;

  @media (max-width: 768px) {
    flex: none;
    align-items: center;
    text-align: center;
    order: 2;
    gap: 15px;
  }
`;

const Title = styled.h1`
  font-size: 74px;
  color: white;
  margin: 0;
  font-weight: 700;
  line-height: 1.1;

  @media (max-width: 1200px) {
    font-size: 60px;
  }

  @media (max-width: 768px) {
    font-size: 36px;
  }

  @media (max-width: 480px) {
    font-size: 28px;
  }
`;

const WhatWeDo = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;

  @media (max-width: 768px) {
    justify-content: center;
  }
`;

const Line = styled.img`
  height: 5px;
  width: 80px;

  @media (max-width: 768px) {
    width: 60px;
    height: 3px;
  }
`;

const Subtitle = styled.h2`
  color: #da4ea2;
  font-size: 24px;
  margin: 0;
  font-weight: 500;

  @media (max-width: 768px) {
    font-size: 20px;
  }

  @media (max-width: 480px) {
    font-size: 18px;
  }
`;

const Desc = styled.p`
  font-size: 20px;
  color: lightgray;
  line-height: 1.5;
  margin: 0;

  @media (max-width: 768px) {
    font-size: 16px;
    max-width: 400px;
  }

  @media (max-width: 480px) {
    font-size: 14px;
  }
`;

const Button = styled.button`
  background-color: #da4ea2;
  color: white;
  font-weight: 500;
  width: 120px;
  padding: 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
  min-height: 44px;

  &:hover {
    background-color: #c7449a;
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }

  @media (max-width: 768px) {
    width: 140px;
    padding: 16px;
  }
`;

const Right = styled.div`
  flex: 3;
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;

  @media (max-width: 768px) {
    flex: none;
    height: 50vh;
    width: 100%;
    order: 1;
  }

  @media (max-width: 480px) {
    height: 40vh;
  }
`;

const Img = styled.img`
  width: 600px;
  height: 450px;
  object-fit: contain;
  animation: animate 2s infinite ease alternate;

  @media (max-width: 1200px) {
    width: 500px;
    height: 375px;
  }

  @media (max-width: 768px) {
    width: 300px;
    height: 225px;
  }

  @media (max-width: 480px) {
    width: 250px;
    height: 188px;
  }

  @keyframes animate {
    to {
      transform: translateY(20px);
    }
  }
`;

const Hero = () => {
  const handleLearnMore = () => {
    window.open('https://Techwayurself.com', '_blank', 'noopener,noreferrer');
  };

  return (
    <Section>
      <Navbar />
      <Container>
        <Left>
          <Title>Think. Create. Solve.</Title>
          <WhatWeDo>
            <Line
              src="./img/line.png"
              alt="Decorative line"
              onError={(e) => {
                e.target.style.display = 'none'
              }}
            />
            <Subtitle>Embrace the Cloud.</Subtitle>
          </WhatWeDo>
          <Desc>
            Skyrocket your business to the clouds with AWS Architecture-based Solutions.
          </Desc>
          <Button onClick={handleLearnMore}>
            Learn More
          </Button>
        </Left>

        <Right>
          <Img
            src="./img/moon.png"
            alt="Johnathan CloudSpace Logo"
            onError={(e) => {
              e.target.alt = 'Logo image not found'
              e.target.style.opacity = '0.3'
            }}
          />
        </Right>
      </Container>
    </Section>
  );
};

export default Hero;