import React from 'react'
import styled from 'styled-components'
import Hero from './components/Hero'
import Who from './components/Who'
import Works from './components/Works'
import Contact from './components/Contact'

const Container = styled.div`
  height: 100vh;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  overflow-y: auto;
  scrollbar-width: none;
  color: white;
  background: url("./img/bg.jpg");

  &::-webkit-scrollbar {
    display: none;
  }

  /* Mobile optimizations */
  @media (max-width: 768px) {
    scroll-snap-type: none;
    overflow-x: hidden;
  }
`

function App() {
  return (
    <Container>
      <Hero />
      <Who />
      <Works />
      <Contact />
    </Container>
  )
}

export default App