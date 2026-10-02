import { useEffect, useRef } from 'react'
import * as THREE from 'three'

export default function AuthVisual() {
  const mountRef = useRef(null)

  useEffect(() => {
    const mount = mountRef.current
    if (!mount) return undefined
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100)
    camera.position.z = 5.2
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.setSize(360, 360)
    mount.appendChild(renderer.domElement)

    const group = new THREE.Group()
    scene.add(group)
    const core = new THREE.Mesh(new THREE.IcosahedronGeometry(1.05, 2), new THREE.MeshBasicMaterial({ color: 0x55d6d1, wireframe: true, transparent: true, opacity: .72 }))
    group.add(core)
    const inner = new THREE.Mesh(new THREE.IcosahedronGeometry(.7, 1), new THREE.MeshBasicMaterial({ color: 0x15383b, transparent: true, opacity: .88 }))
    group.add(inner)
    const ringMaterial = new THREE.MeshBasicMaterial({ color: 0x709cff, transparent: true, opacity: .46, side: THREE.DoubleSide })
    const ringOne = new THREE.Mesh(new THREE.TorusGeometry(1.55, .012, 8, 96), ringMaterial)
    const ringTwo = new THREE.Mesh(new THREE.TorusGeometry(1.86, .008, 8, 96), new THREE.MeshBasicMaterial({ color: 0x80d69b, transparent: true, opacity: .4 }))
    ringOne.rotation.x = Math.PI / 2.8
    ringTwo.rotation.x = Math.PI / 2.8
    ringTwo.rotation.y = Math.PI / 3
    group.add(ringOne, ringTwo)

    const particleGeometry = new THREE.BufferGeometry()
    const positions = new Float32Array(90 * 3)
    for (let index = 0; index < positions.length; index += 3) {
      const radius = 2.1 + Math.random() * .8
      const angle = Math.random() * Math.PI * 2
      const height = (Math.random() - .5) * 3.5
      positions[index] = Math.cos(angle) * radius
      positions[index + 1] = height
      positions[index + 2] = Math.sin(angle) * radius
    }
    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    const particles = new THREE.Points(particleGeometry, new THREE.PointsMaterial({ color: 0x55d6d1, size: .025, transparent: true, opacity: .68 }))
    scene.add(particles)

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    let frameId
    const animate = () => {
      if (!reducedMotion) {
        group.rotation.y += .0028
        group.rotation.x = Math.sin(Date.now() * .00035) * .12
        particles.rotation.y -= .0008
      }
      renderer.render(scene, camera)
      frameId = requestAnimationFrame(animate)
    }
    animate()
    return () => { cancelAnimationFrame(frameId); renderer.dispose(); particleGeometry.dispose(); mount.removeChild(renderer.domElement) }
  }, [])

  return <div className="auth-visual" ref={mountRef} aria-hidden="true" />
}
