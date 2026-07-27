import { io } from 'socket.io-client'

export function initSocket() {
	let host = window.location.hostname
	let siteName = window.site_name || host
	let socketioPort = window.socketio_port || 9000
	let port = window.location.port ? `:${socketioPort}` : ''
	let protocol = port ? 'http' : 'https'
	let url = `${protocol}://${host}${port}/${siteName}`

	let socket = io(url, {
		withCredentials: true,
		reconnectionAttempts: 5,
	})
	return socket
}
